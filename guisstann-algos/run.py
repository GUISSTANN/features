from argparse import ArgumentParser
import pyspark.sql as sql
import pyspark.ml as ml
from pyspark.sql.functions import col
from pyspark.sql.functions import explode

OUTPUT_DIR = "output"


def is_categorical(df: sql.DataFrame, variable: str) -> bool:
    """
    Détermine si une variable est catégorielle ou numérique
    """
    return df.select(variable).distinct().count() < 10


def run_random_forest(df: sql.DataFrame, variable: str):
    """
    Applique un algorithme de forêt aléatoire
    """
    string_indexer = ml.feature.StringIndexer(inputCol=variable, outputCol="label")
    feature_columns = [c for c in df.columns if c != variable]
    assembler = ml.feature.VectorAssembler(inputCols=feature_columns, outputCol="features")
    rf = ml.classification.RandomForestClassifier(labelCol=variable, featuresCol="features")
    pipeline = ml.Pipeline(stages=[string_indexer, assembler, rf])
    train_df, test_df = df.randomSplit([0.8, 0.2])
    param_grid = ml.tuning.ParamGridBuilder() \
        .addGrid(rf.numTrees, [10, 20, 30]) \
        .addGrid(rf.maxDepth, [5, 10, 15]) \
        .build()
    cross_validator = ml.tuning.CrossValidator(estimator=pipeline,
                                               estimatorParamMaps=param_grid,
                                               evaluator=ml.evaluation.MulticlassClassificationEvaluator(
                                                   labelCol="label",
                                                   metricName="accuracy"),
                                               numFolds=5, seed=42)
    cv_model = cross_validator.fit(train_df)
    cv_model.save(f"{OUTPUT_DIR}/random_forest/cv_model")
    predictions = cv_model.transform(test_df)
    print(predictions.head())
    #predictions.write.csv(f"{OUTPUT_DIR}/random_forest/predictions.csv", header=True)
    for metric in ["accuracy", "f1", "weightedPrecision", "weightedRecall"]:
        evaluator = ml.evaluation.MulticlassClassificationEvaluator(labelCol="label", metricName=metric)
        value = evaluator.evaluate(predictions)
        print(f"{metric}: {value}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--fichier", type=str, help="Fichiers contenant les données à traiter", nargs="+")
    parser.add_argument("--variable", type=str, help="Variable à prédire")
    parser.add_argument("--ignore", type=str, help="Variables à ignorer", nargs="+")
    args = parser.parse_args()

    # Initialisation de Spark
    spark = sql.SparkSession.builder.appName("guisstann-algos").getOrCreate()
    data_df = sql.DataFrame()
    for file in args.fichier:
        data_df = data_df.union(spark.read.csv(file, header=True))
    data_df = data_df.drop(*args.ignore)
    for col_name in data_df.columns:
        data_df = data_df.withColumn(col_name, col(col_name).cast("float"))


    # Détermination du type de variable
    if is_categorical(data_df, args.variable):
        run_random_forest(data_df, args.variable)

    spark.stop()

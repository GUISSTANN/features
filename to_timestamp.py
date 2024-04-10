import pandas as pd


def to_timestamp(data : pd.DataFrame, date_col : str, time_col:str) -> pd.DataFrame :
    """ this function goal is to create a time variable with the correct timestamp according the cider format.
    It use the call_data and the call_time variable from mobile data file.

    Args:
        data (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    data[date_col] = data[date_col].astype("O")
    print(data)
    data["new_date"] = pd.to_datetime(data[date_col], format="%Y%m%d")
    data["year"] = data["new_date"].dt.year
    data["month"] = data["new_date"].dt.month
    data["day"] = data["new_date"].dt.day
    data["second"] = pd.to_numeric(data[time_col].astype('str').str[-2:])
    data["minute"] = pd.to_numeric(data[time_col].astype('str').str[-4:-2])
    data["hour"] = pd.to_numeric(data[time_col].astype('str').str[:-4])

    data["timestamp"] = pd.to_datetime(data[["year", "month","day", "hour", "minute", "second"]])
    data.drop(columns=["year", "month","day", "hour", "minute", "second", "new_date"], inplace=True)
    #print(data.describe())
    #print(data.head())
    return data

if __name__ == "__main__":
    df = pd.read_csv("data/data_mobile/data.csv", index_col=0)
    out_df = to_timestamp(data=df, date_col="call_date", time_col= "call_time")
    print(out_df.head())
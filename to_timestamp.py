import pandas as pd


def to_timestamp(data : pd.DataFrame, date_col : str, time_col:str = None) -> pd.DataFrame :
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
    if time_col != None:
        data["second"] = pd.to_numeric(data[time_col].astype('str').str[-2:])
        data["minute"] = pd.to_numeric(data[time_col].astype('str').str[-4:-2])
        data["hour"] = pd.to_numeric(data[time_col].astype('str').str[:-4])
        data["timestamp"] = pd.to_datetime(data[["year", "month","day", "hour", "minute", "second"]])
        data.drop(columns=["year", "month","day", "hour", "minute", "second", "new_date"], inplace=True)
    else:
        data["timestamp"] = pd.to_datetime(data[["year", "month","day"]])
        data.drop(columns=["year", "month","day","new_date"], inplace=True)
    #print(data.describe())
    #print(data.head())
    return data

if __name__ == "__main__":
    ## MOBILE DATA
    df = pd.read_csv("data/data_mobile/data.csv", index_col=0)
    out_df = to_timestamp(data=df, date_col="call_date", time_col= "call_time")
    out_df.to_csv("output_data/mobile_data.csv")
    # MOBILE MONEY
    df_om = pd.read_csv("data/transactions/om.csv", index_col=0)
    om_out_df = to_timestamp(data=df_om, date_col="transfer_date", time_col="transfer_time")
    om_out_df.to_csv("output_data/mobilemoney.csv")
    print(om_out_df.head())
    # RECHARGE
    rech_df = pd.read_csv("data/recharges/recharges.csv", index_col=0)
    rech_out = to_timestamp(data=rech_df, date_col="call_event_date")
    print(rech_df.head())
    rech_out.to_csv("output_data/recharge.csv")

    # Voix SMS OFF
    voix_off_df = pd.read_csv("data/voix_sms/voix_sms_offnet.csv", index_col=0)
    voix_off_out = to_timestamp(data=voix_off_df, date_col="call_date", time_col="call_time")
    print(voix_off_out.head())
    voix_off_out.to_csv("output_data/voix_sms_offnet.csv")

    # VOIX SMS ON

    voix_on_df = pd.read_csv("data/voix_sms/voix_sms_onnet.csv", index_col=0)
    voix_on_out = to_timestamp(data=voix_on_df, date_col="call_date", time_col="call_time")
    print(voix_on_out.head())
    voix_on_out.to_csv("output_data/voix_sms_onnet.csv")
import pandas as pd
import numpy as np
import datetime

# Adds survival times of each observation in the "survival_time" column
def add_survival_time(df): 
    df['survival_time'] = df.apply(lambda row: row["mth_code"] - row["snapshot"] if row["mth_code"] // 100 == row["snapshot"] // 100 else (row["mth_code"] % 100) - (row["snapshot"] % 100) + 12, axis=1)
    return df

# Gives each month a number from month 1 (January 2018) to month 24 (December 2019) and stores these values in the "month_num" column
def add_month_nums(df):
    df['month_num'] = np.where(df['mth_code'] // 100 == 2018, df['mth_code'] % 100, df['mth_code'] % 100 + 12)
    return df

# Sorts the observations in ascending order by the "snapshot" and "mth_code" columns
def sort_by_mth_and_snapshot(df):
    df = df.sort_values(by=["snapshot"], ascending = True)
    df = df.sort_values(by=["mth_code"], ascending = True)
    return df

# Only keeps one occurence of each observation which is when it gets charged off or its last occurrence if it doesn't gets charged off over the entire time period
def get_uniques(df):
    df['max_survival_time'] = df.apply(lambda row: 201912 - row['snapshot'] if row['snapshot'] // 100 == 2019 else (201912 % 100) - (row['snapshot'] % 100) + 12, axis=1)
    df = df[(df.charge_off == 1) | (df.survival_time == df.max_survival_time)]
    return df

# Returns the monthcode of the input as a string
def add_mths(input: str, n: int):
    input = (int)(input)
    last_two = input % 100
    input -= last_two
    if last_two + n > 12:
        input += 100
        input += (last_two + n) % 12
    else: 
        input += (last_two + n)
    return (str)(input)

# Formats monthcode from date
def format_date(input: str):
    x = ""
    if len(input) == 9:
        x = input[-4:] + "0" + input[0]
    elif len(input) == 10:
        x = input[-4:] + input[0:2]
    else:
        raise Exception("Problem with input")
    # return add_mths(x, 6)
    return x
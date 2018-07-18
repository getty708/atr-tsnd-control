# -----------------------------------------------------------------------
# Name: log_to_ADL.py
# Author: Yoshimura Naoya
# Created: 2018.05.23
# Copyright:   (c) yoshimura 2018
#
# Purpose: Convert raw log file into ADLtagger format (csv)
#
# -----------------------------------------------------------------------

import os
import argparse
import pandas as pd
import numpy as np

import datetime as dt
import csv

# -------------------------------------------------------------
""" Command Line Arguments
"""
def make_parser():
    parser = argparse.ArgumentParser(
        description="Convert Log file into ADLtagger format"
    )

    # Add Arguments
    parser.add_argument('--sensor', required=True,
                        help="Sensor type, {ags, geo}")
    parser.add_argument('--filename-input', required=True,
                        help="Input log filename (*.log)")
    parser.add_argument('--filename-output', required=True,
                        help="Output filename (*.csv)")
    parser.add_argument('--date', required=True,
                        help="Str(%Y-%m-%d), Date which the log data was recorded.")
    parser.add_argument('--shift', default=0., type=float,
                        help="Milli second to shift csv's timestamp")
    return parser



# -------------------------------------------------------------    
# ======================================
# ==  Load LOG file [ATR log format]  == 
# ======================================
def read_log_file(path_to_log, sensor):
    """ Read a log file and convert it into pd.DataFrame

    Args.
    ------
    - path_to_log: Str, path, [columns="sensor,time_ATR,accX,accY,accZ,gyroX,gyroY,gyroZ"]
    - sensor     : Str, sensor identifier in log file.

    Return
    -------
    - DataFrame
    """
    df = []
    with open(path_to_log, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if sensor in row: df.append(row)
        print(">> Done: Read CSV [path={}, df={}]".format(path_to_log, len(df)))
    if sensor == "ags":
        cols = ["sensor", "time_ATR", "acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"]
    elif sensor == "geo":
        cols = ["sensor", "time_ATR", "geo_x", "geo_y", "geo_z",]
    df = pd.DataFrame(df, columns=cols)
    print(">> Done: df.shape={}".format(df.shape))
    return df



# ============
#  Timestamp
# ============
def add_timestamps(df, base_timestamp):
    """ Add timestamps to each row

    Args.
    -----
    - df: pd.DataFrame
    
    Return.
    -------
    - df: pd.DataFrame, [type(time)=str("%Y%m%d_%H:%M:%S.%fff")]
    """

    def convert_timestamp(time):
        """ Convert an ATR timestamp into a datetime object
        
        Args.
        -----
        - time          : str, timestamp with ATR format (Miliseconds from 0:00)
        (- base_timestamp: datetime, this is needed for synconization with video data)
        
        Return
        ------
        - datetime object
        """    
        # Convert milliseconds to r60
        time = int(time)
        milliseconds, time = time%1000, int(time/1000)
        seconds,      time = time%60,   int(time/60)
        minutes,      time = time%60,   int(time/60)
        hours,        time = time%60,   int(time/60)
        # Error Check
        if time > 1:
            print(">> Error: timestamp of ATR sensor is invaild format.")
        # 基準時間と合わせる
        new_time = base_timestamp + dt.timedelta(milliseconds=milliseconds, seconds=seconds, minutes=minutes, hours=hours)
        return new_time

    # MAIN
    df = df.sort_values(by=["time_ATR"], ascending=True).reset_index(drop=True)
    df["timestamp"] = df["time_ATR"].apply(convert_timestamp) # Convert ADT timestamp to  datatime object
    df["time"], df["time_milli"] = df["timestamp"].dt.strftime('%Y%m%d_%H:%M:%S.'), df["timestamp"].dt.microsecond // 1000
    df["time"] = df["time"].astype(str) + df["time_milli"].astype(str).str.zfill(3) # '%Y%m%d_%H:%M:%S.' + '%fff'
    print(">> Done: df.shape={}".format(df.shape))
    return df




        
# -------------------------------------------------------------
def main():
    parser = make_parser()
    args = parser.parse_args()
    print("< Args >")
    print(args, "\n\n")

    
    # Params
    print("Start: Init parms")
    base_timestamp = dt.datetime.strptime(args.date, '%Y-%m-%d') + dt.timedelta(milliseconds=float(args.shift))
    print(">> Done: base_timestamp={}".format(base_timestamp))
    print(">> Success\n")
    
    # Raed Input file
    print("Start: Read and convert log files to pd.DataFrame")
    df = read_log_file(args.filename_input, args.sensor)
    print(df.head())
    print(">> Success\n")

    # Add timestamp
    print("Start: Add timestamp")
    df = add_timestamps(df, base_timestamp)
    print(df.head())
    print(">> Success\n")

    # Convert Unit
    if args.sensor == "ags":
        df[["acc_x","acc_y","acc_z",]]    = df[["acc_x","acc_y","acc_z",]].astype(float)    / 10000.
        df[["gyro_x","gyro_y","gyro_z",]] = df[["gyro_x","gyro_y","gyro_z",]].astype(float) / 100.
    elif args.sensor == "geo":
        df[["geo_x","geo_y","geo_z",]]    = df[["geo_x","geo_y","geo_z",]].astype(float)    / 10.**(7)
    

    # Write
    print("Start: Write CSVs.")
    df["label"], df["label_id"] = "none", -1
    if args.sensor == "ags":
        cols = ["time","label","label_id","acc_x","acc_y","acc_z","gyro_x","gyro_y","gyro_z"]
    elif args.sensor == "geo":
        cols = ["time","label","label_id","geo_x","geo_y","geo_z",]
    df = df[cols]
    df.to_csv(args.filename_output, index=False)
    print(">> Done: Write csv.[{}, {}]".format(df.shape, args.filename_output))
    print(df.head(10))
    print(">> Success\n")
    
    
# -------------------------------------------------------------
if __name__=='__main__':
    main()

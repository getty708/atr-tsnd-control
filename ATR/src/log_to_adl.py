# -----------------------------------------------------------------------
# Name: ADL_to_csv.py
# Author: Yoshimura Naoya
# Created: 2018.05.23
# Copyright:   (c) yoshimura 2018
#
# Purpose: Convert ADLtagger-format csv into single CSV
#
# -----------------------------------------------------------------------

import os
import shutil # shutil.rmtree(path)でdirectory tree全体を削除(空でなくても)
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
    parser.add_argument('--path-input-log', required=True,
                        help="A path to an input log file.")
    parser.add_argument('--date', required=True,
                        help="Str(%Y-%m-%d), Date which the log data was recorded.")
    parser.add_argument('--shift', required=True,
                        help="Milli second to shift csv's timestamp")
    parser.add_argument('--path-output-dir', required=True,
                        help="A path to an output log file.")
    return parser



# -------------------------------------------------------------
def read_log_file(path_to_log):
    """ Read a log file and convert it into pd.DataFrame

    Args.
    ------
    - path_to_log: Str, path, [columns="sensor,time_ATR,accX,accY,accZ,gyroX,gyroY,gyroZ"]

    Return
    -------
    - DataFrame
    """
    df = []
    with open(path_to_log, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if "ags" in row: df.append(row)
        print(">> Done: Read CSV [path={}, df={}]".format(path_to_log, len(df)))
    df = pd.DataFrame(df, columns=["sensor", "time_ATR", "accX", "accY", "accZ", "gyroX", "gyroY", "gyroZ"])
    print(">> Done: df.shape={}".format(df.shape))
    return df



# -------------------------------------------------------------
# ============
#  Timestamp
# ============
def add_timestamps(df, base_timestamp):
    """ Add timestamps to each row

    Args.
    -----
    - df: pd.DataFrame
    """

    def generate_timestamp(time):
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
    df["timestamp"] = df["time_ATR"].apply(generate_timestamp) # Convert ADT timestamp to  datatime object
    df["time"], df["time_milli"] = df["timestamp"].dt.strftime('%Y%m%d_%H:%M:%S.'), df["timestamp"].dt.microsecond // 1000
    df["time"] = df["time"].astype(str) + df["time_milli"].astype(str).str.zfill(3)
    df["group"] = df["timestamp"].dt.strftime('%Y%m%d_%H%M')
    print(">> Done: df.shape={}".format(df.shape))
    return df



# -------------------------------------------------------------
# ============
#  Output
# ============
def setup_dir(path):
    """ Clean

    Args.
    ------
    - pathr: path
    """
    if not os.path.isdir(path):
        # If selected DIR does not exist, create it.
        os.makedirs(path)
        if os.path.isdir(path):
            print(">> Done: create directory [{}]".format(path))
    return path


def write_csv(df, path_output_dir):
    groups = df["group"].drop_duplicates().reset_index(drop=True)
    # Clean ouput directory
    if os.path.isdir(path_output_dir):
        shutil.rmtree(path_output_dir)
        os.mkdir(path_output_dir)
        print(">> Done: Clean output directory") 
    for group in groups:
        #　書き込む行を選択
        df_selected = df[df["group"] == group].sort_values(by=["timestamp"])
        # 書き込むディレクトリを選択: Acc
        ## ディレクトリの確認
        target_path = setup_dir(os.path.join(path_output_dir, "acc2", "acc2_R"))
        # target_path = self.activate_dir(os.path.join(target_path, "acc2_R"))
        ## 書き込みファイルを指定
        target_file_name = group+"00_acc2.csv"
        # CSV書き込み
        filename = os.path.join(target_path, target_file_name)
        df_selected[["time", "accX", "accY", "accZ"]].to_csv(filename, index=False, header=["time", "x", "y", "z"])
        print(">> write", target_path+target_file_name)

        # 書き込むディレクトリを選択: Gyro
        ## ディレクトリの確認
        target_path = setup_dir(os.path.join(path_output_dir, "Gyro", "gyro"))
        ## 書き込みファイルを指定
        target_file_name = group+"00_gyro.csv"
        # CSV書き込み
        filename = os.path.join(target_path, target_file_name,)
        df_selected[["time", "gyroX", "gyroY", "gyroZ"]].to_csv(filename, index=False, header=["time", "x", "y", "z"])
        print(">> Done: write", target_path+target_file_name)
    return len(groups)


    
# -------------------------------------------------------------
def main():
    # Parse Command Line Argumenmts
    parser = make_parser()
    args = parser.parse_args()

    # Params
    print("Start: Init parms")
    base_timestamp = dt.datetime.strptime(args.date, '%Y-%m-%d') + dt.timedelta(milliseconds=float(args.shift))
    print(">> Done: base_timestamp={}".format(base_timestamp))
    print(">> Success\n")
    
    # Raed Input file
    print("Start: Read and convert log files to pd.DataFrame")
    df = read_log_file(args.path_input_log)
    print(df.head())
    print(">> Success\n")

    # Add timestamp
    print("Start: Add timestamp")
    df = add_timestamps(df, base_timestamp)
    print(df.head())
    print(">> Success\n")

    # Write
    print("Start: Write CSVs.")
    n_files = write_csv(df, args.path_output_dir)
    print(">> Success: {} files were created\n".format(n_files))
    
    
# -------------------------------------------------------------
if __name__=='__main__':
    main()

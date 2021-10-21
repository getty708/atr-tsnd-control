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

import xml.etree.ElementTree as ET
import datetime as dt


# -------------------------------------------------------------
""" Command Line Arguments
"""
def make_parser():
    parser = argparse.ArgumentParser(
        description="Convert Log file into ADLtagger format"
    )
    subparsers =  parser.add_subparsers(title="Sub-Commands")

    # Add Arguments
    ## single
    single_parser = subparsers.add_parser("SINGLE")
    single_parser.set_defaults(func=main_single)
    single_parser.add_argument('--path-input-root-dir', required=True,
                               help="Path to the root directory for input")
    single_parser.add_argument('--path-input-xml', required=True,
                               help="Path to the label XML file")
    single_parser.add_argument('--path-output-dir', required=True,
                               help="Path to the root directory for output")
    single_parser.add_argument('--filename-csv', required=True,
                               help="Output filename for Sensor data CSV")
    single_parser.add_argument('--filename-label', required=True,
                               help="Output filename for Label data. If you don't use label, set None")
    single_parser.add_argument('--filename-summary', required=True,
                               help="Output filename for Label summary csv")

    ## Mix
    mix_parser = subparsers.add_parser("MIX")
    mix_parser.set_defaults(func=main_mix)
    mix_parser.add_argument('--path-input-root-dir-acc', required=True,
                            help="Path to the root directory for acc input")
    mix_parser.add_argument('--path-input-root-dir-gyro', required=True,
                            help="Path to the root directory for gyro input")
    mix_parser.add_argument('--path-input-xml', required=True,
                            help="Path to the label XML file")
    mix_parser.add_argument('--path-output-dir', required=True,
                            help="Path to the root directory for output")
    mix_parser.add_argument('--filename-csv', required=True,
                            help="Output filename for Sensor data CSV")
    mix_parser.add_argument('--filename-label', required=True,
                            help="Output filename for Label data. If you don't use label, set None")
    mix_parser.add_argument('--filename-summary', required=True,
                            help="Output filename for Label summary csv")
    
    return parser




# -------------------------------------------------------------    
# ===================================
# ==  Load CSV files [ADL format]  == 
# ===================================
def get_csv_with_BFS(df, current_path):
    """ Get csv files with BFS algolithm
    """
    # 現在のディレクトリにあるディレクトリを取得
    for x in os.listdir(current_path):
        path_next = os.path.join(current_path, x)
        print(">> >>", path_next)
        if os.path.isdir(path_next):
        # ディレクトリが存在する場合 ==> より深く潜る
            df = get_csv_with_BFS(df, path_next)
        elif os.path.isfile(path_next):
            # ファイル場合 ==> CSVか判定 ==> YES: dfに追加
            root, extention = os.path.splitext(x)
            if extention == ".csv":
                df = pd.concat([df, pd.read_csv(path_next)])
    return df


def read_csv(path_to_root_dir, fix_timestamp=True):
    # CSV files
    df = pd.DataFrame()
    df = get_csv_with_BFS(df, path_to_root_dir)
    print(">> Done: read CSV files [df={}]".format(df.shape))
    #  timestampの桁落ちを修正
    print(">> fix timestamp = ", fix_timestamp)
    if fix_timestamp:
        df_tmp = df[["time"]].copy()
        df_tmp["time_1"] = "none"
        df_tmp["time_2"] = "none"
        df_tmp[["time_1","time_2"]] = df_tmp["time"].str.split(".", expand=True)
        df["time"] = df_tmp["time_1"] + "." +df_tmp["time_2"].str.zfill(3)
        print(">> Done: fix timestamp [restore significant digits]") # 桁落ちの修正
    df = df.sort_values(by=["time"]).reset_index(drop=True)
    print(">> Done: read sensor data  [df={}]".format(df.shape)) # 桁落ちの修正
    return df


# ===============================
# ==  Load Label data  [.xml]  == 
# ===============================
def parse_time_str(s):
        try:
            ymd, HMS, ms = s[0:10].replace('-', ''), s[11:19], s[20:]
        except IndexError as e:
            ymd, HMS, ms = s[0:10].replace('-', ''), s[11:19], '000'
        return str(ymd)+'_'+str(HMS)+'.'+str(ms).ljust(3, '0')

    
def read_label_xml(path_to_xml):
    """ Read [Load] label data which is generated by ADLtagger.
    Args
    ----
    - path_xml_file: path

    Return
    -------
    - pd.DataFrame
    """
    tree = ET.parse(path_to_xml)
    elem = tree.getroot()
    df_label = []
    for e in elem.findall("labellist"):
        label = e.find("eventtype").text
        start = parse_time_str(e.find("start").text)
        end = parse_time_str(e.find("end").text)
        df_label.append([label, start, end])
    df_label = pd.DataFrame(df_label, columns=["label", "start", "end"])
    print(">> Done: read label XML  [df_label={}]".format(df_label.shape)) # 桁落ちの修正        
    return df_label


# ================================
# ==  Merge csv and label data  == 
# ================================
def merge_label(df, df_label):
    # timedelta型に変換
    df["time"]        = pd.to_datetime(df["time"], format="%Y%m%d_%H:%M:%S.%f") 
    df_label["start"] = pd.to_datetime(df_label["start"], format="%Y%m%d_%H:%M:%S.%f")
    df_label["end"]   = pd.to_datetime(df_label["end"], format="%Y%m%d_%H:%M:%S.%f")
    
    labels, label_ids = ["none" for i in range(len(df)) ], [-1 for i in range(len(df)) ]
    for i in range(len(df_label)):
        label, start, end = df_label.loc[i,"label"], df_label.loc[i,"start"], df_label.loc[i,"end"]
        index = df[(df["time"] >= start) & (df["time"] <= end)].index
        # label配列を修正
        for j in index:
            labels[j], label_ids[j] = label, i
        if i%50 == 0:
            print(">> >> Done: id={}, Label=`{:<10}`, Time=[{}, {}]".format(str(i).zfill(4), label, start, end))
    df["label"], df["label_id"] = labels, label_ids
    print(">> Done: merge sensor data and label data [df={}]".format(df.shape))
    return df


# ============
# ==  Write == 
# ============
def write_csv(df, path_output_dir, file_name):
    # setup directory
    if not os.path.isdir(path_output_dir):
        os.mkdir(path_output_dir)
    # Write
    path_csv = os.path.join(path_output_dir, file_name)
    df.to_csv(path_csv, index=False)
    print(">> Done: Write csv.[{}]".format(path_csv))


def write_labels(df_label, path_output_dir, filename_label, filename_summary):
    # setup directory
    if not os.path.isdir(path_output_dir):
        os.mkdir(path_output_dir)
    # Write
    ## Label
    path_csv = os.path.join(path_output_dir, filename_label)
    df_label.to_csv(path_csv)
    print(">> Done: Write label data to [{}]".format(path_csv))
    ## Summary of label
    df_summary = df_label[["label", "start"]].groupby(by=["label"]).count().sort_values(["start"], ascending=False)
    path_csv = os.path.join(path_output_dir, filename_summary)
    df_summary.to_csv(path_csv)
    print(">> Done: Write label summary to [{}]".format(path_csv))
    print(df_summary)

    



        
# -------------------------------------------------------------
def main_single(args):
    """ Convert single sensor data
    """
    # Load data
    print("Start: Read csv files and label xml data.")
    df = read_csv(args.path_input_root_dir)   # sensor data [CSV]
    df_label = read_label_xml(args.path_input_xml)  # label  data [XML]
    print(">> Success: Read Data[df={}. df_label={}]\n".format(df.shape, df_label.shape))

    # Merge sensor data and label data
    print("Start: Add label to sensor data.")
    df = merge_label(df, df_label)
    print(df.head(10))
    print(">> Success: df.shape={}\n".format(df.shape))

    # Write
    print("Start: Write CSV files")
    write_csv(df, args.path_output_dir, args.filename_csv)
    write_labels(df_label, args.path_output_dir, args.filename_label, args.filename_summary)
    print(">> Success\n")
    print("Finish !!\n")


    
def main_mix(args, merge_with_timestamp=False):
    """ Convert acc&gyro and write into single file
    """
    # Param
    add_label = False if args.path_input_xml == "None" else True
    # Load data
    print("Start: Read csv files and label xml data.")
    df_acc = read_csv(args.path_input_root_dir_acc)   # sensor data [Acc CSV]
    df_gyro = read_csv(args.path_input_root_dir_gyro)   # sensor data [Gryro CSV]
    if add_label:
        df_label = read_label_xml(args.path_input_xml)  # label  data [XML]
    else:
        df_label = pd.DataFrame()
    ## Rename Columns
    df_acc  = df_acc.rename(columns={"x":"acc_x","y":"acc_y","z":"acc_z"})
    df_gyro = df_gyro.rename(columns={"x":"gyro_x","y":"gyro_y","z":"gyro_z"})
    print(df_acc.head(10))
    print(df_gyro.head(10))
    print(">> Success: Read Data[df_acc={}, df_gyro={}, df_label={}]\n".format(df_acc.shape, df_gyro.shape, df_label.shape))

    # Merge sensor data and label data
    if add_label:
        print("Start: Add label to sensor data.")
        df_acc = merge_label(df_acc, df_label)
        print(df_acc.head(10))
        print(df_gyro.head(10))
        print(">> Success: df_acc.shape={}\n".format(df_acc.shape))
    else:
        df_acc["time"] = pd.to_datetime(df_acc["time"], format="%Y%m%d_%H:%M:%S.%f")
        df_acc["label"], df_acc["label_id"] = "none", -1

    # Merge Acc & Gyro
    print("Start: Merge Acc & Gyro")
    df_gyro["time"] = pd.to_datetime(df_gyro["time"], format="%Y%m%d_%H:%M:%S.%f")
    if merge_with_timestamp:
        df = pd.merge(df_acc, df_gyro, on=["time"], how="left")
    else:
        assert df_acc.shape[0] == df_gyro.shape[0], ">> Error: lengths of each DataFrame is not matched [df_acc={}, df_gyro={}]".format(df_acc.shape, df_gyro.shape)
        df = pd.concat([df_acc, df_gyro[["gyro_x","gyro_y","gyro_z"]]], axis=1)
    ## Excahnge the order of columns
    cols = ["time","label","label_id", "acc_x","acc_y","acc_z", "gyro_x","gyro_y","gyro_z"]
    df = df[cols]
    
    print(df.head())
    print(">> Success: df.shape={}\n".format(df.shape))
    
    
    # Write
    print("Start: Write CSV files")
    write_csv(df, args.path_output_dir, args.filename_csv)
    if add_label and not (args.filename_label == "None"):
        write_labels(df_label, args.path_output_dir, args.filename_label, args.filename_summary)
    print(">> Success\n")
    print("Finish !!\n")
    



def main():
    parser = make_parser()
    args = parser.parse_args()
    print("< Args >")
    print(args, "\n\n")
    args.func(args)
    
    
# -------------------------------------------------------------
if __name__=='__main__':
    main()

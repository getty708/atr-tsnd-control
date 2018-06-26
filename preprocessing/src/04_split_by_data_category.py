# -----------------------------------------------------------------------
# Name: 04_split_by_data_category.py
# Author: Yoshimura Naoya
# Created: 2018.01.18
# Copyright:   (c) yoshimura 2017
#
# Purpose: Reshape labeled frames into DNN input style.
# -----------------------------------------------------------------------

import pandas as pd
import numpy as np
import argparse


"""Params
"""
sensor = "acc"
f_shape = (64, 1) # @100 Hz
root_dir = "./dataStore/n{}/".format(f_shape[0])

# Name list
# name_list = [
#     "01_kawabe",   "02_higashinaka", "03_yasuda", "04_kamiya",
#     "05_ishiyama", "06_yoshimura",   "07_aiko",   "08_higashide",
#     "09_others",   "10_others",      "11_others", "12_others",
#     "13_others",   "14_others",      "15_others",
#     "16_others", "17_others",
# ]
# name_list = [
#     "30_hada", "31_teramae","32_torisuke", "33_matsukawa","34_sato","35_hamase",
#     "36_yamasaki","37_koguchi","38_onuma","39_kashiyama","40_yamaguchi",
#     "41_watase","42_oga","43_shigeyoshi","44_hukuda","45_maekawa",
# ]



""" make parser
"""
def make_parser():
    """Initialize command line arguments
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Sub-Commands')

    # Single 
    single_parser = subparsers.add_parser('SINGLE')
    single_parser.set_defaults(func=handle_single_user)
    parser.add_argument('--user',  required=True,
                             help='a sub_id of the user(int)')
    single_parser.add_argument('--data-category',  required=True,
                               help='{gesture, object, none}')    

    # All
    all_parser = subparsers.add_parser('all')
    all_parser.set_defaults(func=handle_all_users)
    all_parser.add_argument('--data-category',  required=True,
                               help='{gesture, object, none}')
    
    return parser



""" Add labels to ``none'' label frames: Bugfix is needed (to adopt new label id format). 
"""
def add_index_to_none_label(df, df_label, mod, axis, sub_id, label_id_none):
    def label_none(df, start_time, end_time, sub_label_id_none):
        if start_time > end_time:
            print("Error: invalid time. start_time={}, end_time={}".format(start_time, end_time))
        # modを合わせる
        mod_start = (start_time.microsecond / 1000)%5
        mod_end   = (end_time.microsecond   / 1000)%5
        new_start_time = start_time - dt.timedelta(microseconds=(mod_start - mod_end)*1000)
        # index
        idx_start = df[df["start_time"] == new_start_time].index
        idx_end   = df[df["start_time"] == end_time].index
        if (len(idx_start) != 1) or (len(idx_end) != 1):
            print("Error: too many idx.", idx_start, idx_end)
            print("start_time={}, end_time={}".format(new_start_time, end_time))
        idx_start, idx_end = idx_start[0], idx_end[0]
        for idx in range(idx_start, idx_end-128, 128):
            df.loc[idxx:idx+127, "sub_label_id"] = label_id_none
            df.loc[idx:idx+127, "no"] = range(128)
            sub_label_id_none -= 1
        return df, label_id_none
    
    # add label
    df_label_tmp = df_label[(df_label["sub_id"] == sub_id)].reset_index(drop=True)
    cols =  ["label_id", "cat", "label", "end",]
    for i in range(len(df_label_tmp)-1):
        (label_id_start, cat_start, label_start, none_start_time) = df_label_tmp.loc[i,cols]
        (label_id_end,   cat_end,   label_end,   none_end_time) = df_label_tmp.loc[i+1,cols]
        df, label_id_none = label_none(df, none_start_time, none_end_time, label_id_none)
    return df



""" Frame Extaction
"""
def extract_gesture_data(df):
    df_tmp = df[df["cat"] == "gesture"]
    return df_tmp

def extract_object_data(df):
    df_tmp = df[df["cat"] == "object"]
    return df_tmp

def extract_none_data(df):
    # # Add labels
    # sub_label_id_none = -2
    # df_tmp = add_index_to_none_label(df, df_label, mod, axis, sub_id, sub_label_id_none)
    # # Select
    # df_tmp = df_tmp[(df["label"] == "none") & (df_tmp["label_id"] < -1)]
    df_tmp = df[df["cat"] == "none"]    
    return df_tmp



""" 
Main
"""
def handle_single_user(_args, sub_id=None):
    if not sub_id:
        _name = name_list[int(_args.user)- 1]
        sub_id = _name.split("_")[0]
    for mod in range(5):
        for axis in ["x", "y", "z"]:
            # Read CSV
            file_name = './dataStore/n{}_labeled/mg4_200Hz_sub{}_mod{}_{}_{}.csv'.format(
                f_shape[0], sub_id, mod, sensor, axis)
            print("File name: ", file_name)
            df = pd.read_csv(file_name, index_col=0)
            df["sub_id"] = df["sub_id"].astype(str).str.zfill(2)
            # Select
            if _args.data_category == "gesture":
                df_tmp = extract_gesture_data(df)                     
            elif _args.data_category == "object":
                df_tmp = extract_object_data(df)
            elif _args.data_category == "none":
                df_tmp = extract_none_data(df)
            # Add labels
            file_name_out = './dataStore/n64_{}/mg4_200Hz_sub{}_mod{}_{}_{}.csv'.format(_args.data_category,sub_id, mod, sensor,axis)
            df_tmp.to_csv(file_name_out, index=True)
            print(">> Success: {} [df_tmp.shape={}]\n".format(file_name_out, df_tmp.shape))



def handle_all_users(_args):
    for _name in name_list[:]:
        sub_id = _name.split("_")[0]
        handle_single_user(_args, sub_id=sub_id)


# ------------------------------------------------------------------------
def main():
    parser = make_parser()
    args = parser.parse_args()
    print("Args:", args)
    print("\n")
    args.func(args)


# ------------------------------------------------------------------------
if __name__=='__main__':
    main()
    

            

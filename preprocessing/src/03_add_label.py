# -----------------------------------------------------------------------
# Name: add_label.py
# Author: Yoshimura Naoya
# Created: 2018.01.18
# Copyright:   (c) yoshimura 2017
#
# Purpose: make inputs frames from 200Hz sequence 
# -----------------------------------------------------------------------

import pandas as pd
import numpy  as np
import datetime as dt

import argparse

#
# Params
#

""" make paser
"""
def make_parser():
    """Initialize command line arguments
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Sub-Commands')


    # Single 
    single_parser = subparsers.add_parser('single')
    single_parser.set_defaults(func=handle_single_user)
    single_parser.add_argument('--user',  required=True,
                             help='a sub_id of the user(int)')
    single_parser.add_argument('--label-info',  default='None',
                             help='a path to label info')


    # All
    all_parser = subparsers.add_parser('all')
    all_parser.set_defaults(func=handle_all_users)

    return parser



""" Add labels
"""
def label_gesture(df, label_id, cat, label, start_time, session):
    """ Add labels to single ``gesture'' sequence
    """
    idx = df[df["start_time"] == start_time].index
    if len(idx) != 1:
        print("Error: too many idx.", idx)
    idx = idx[0]
    df.loc[idx:(idx+64*2-1), "label"] = label
    df.loc[idx:(idx+64*2-1), "label_id"] = label_id
    df.loc[idx:(idx+64*2-1), "session"] = session
    df.loc[idx:(idx+64*2-1), "cat"] = cat
    df.loc[idx:(idx+64*2-1), "no"] = range(64*2)
    return df


def label_other(df, label_id, cat, label, start_time, end_time, session=-1):
    """ Add label to single ``Object'', ``none'', and ``control'' sequence
    """    
    # Index
    idx_start = df[df["start_time"] == start_time].index
    idx_end   = df[df["start_time"] == end_time].index
    if (len(idx_start) != 1) or (len(idx_end) != 1):
        print("\nError: too many idx.", idx_start, idx_end, "\n")
    idx_start, idx_end = idx_start[0], idx_end[0]
    df.loc[idx_start:idx_end, "label"] = label
    df.loc[idx_start:idx_end, "label_id"] = label_id
    df.loc[idx_start:idx_end, "session"] = session   
    df.loc[idx_start:idx_end, "cat"] = cat
    df.loc[idx_start:idx_end, "no"] = range(idx_end-idx_start+1)
    return df


def add_label(df, df_label, mod, axis, sub_id, label_info='None', debug=True):
    """ Add label to entire DataFrame
    """
    #
    # Add labels
    df["label"] = "none"
    df["label_id"] = "--"
    df["session"] = -1
    df["no"] = -1
    df["cat"] = "none"
    if label_info != 'None':
        for i in range(len(df_label)):
            cols_label = ["label_id", "cat", "label", "start_mod{}".format(mod),"end_mod{}".format(mod),"session"] 
            (label_id, cat, label, start_time, end_time, session) = df_label.loc[i, cols_label]
            if cat == "gesture":
                df = label_gesture(df, label_id, cat, label, start_time, session)
            else:
                df = label_other(df,   label_id, cat, label, start_time, end_time, session)
    #
    # Write results
    cols_idx = ["start_time", "sub_id", "label_id", "session", "mod", "cat", "label", "no", "axis"]
    cols_data = ["x_{}".format(j) for j in range(0, f_shape[0]*2)]
    df = df[cols_idx+cols_data]
    if not debug:
        file_name = './dataStore/n64_labeled/mg4_200Hz_sub{}_mod{}_{}_{}.csv'.format(
            sub_id, mod, sensor,axis)
        df.to_csv(file_name, index=True)
        print(">> Done: Write {}".format(file_name))
    return df


""" 
Main
"""
def handle_single_user(_args, sub_id=None):
    #
    # Load label info
    print(">> label_info={}".format(_args.label_info))
    if _args.label_info != 'None':
        df_label = pd.read_csv(_args.label_info)
        # df_label["start"] = pd.to_datetime(df_label["start"], format="%Y%m%d %H:%M:%S.%f")    
        df_label["end"] = pd.to_datetime(df_label["end"], format="%Y%m%d %H:%M:%S.%f") 
        df_label["sub_id"] = df_label["sub_id"].astype(str).str.zfill(2)
        print(df_label.head())

    # 
    # Main
    #
    if not sub_id:
        _name = name_list[int(_args.user)-1]
        sub_id = _name.split("_")[0]
    for mod in range(5):
        for axis in ["x", "y", "z"]:
            # Read CSV
            file_name = './dataStore/n{}/mg4_200Hz_sub{}_mod{}_{}_{}_framed.csv'.format(
                f_shape[0], sub_id, mod, sensor, axis)
            print("File name: ", file_name)
            print(">> sub_id = {}, mod = {}".format(sub_id, mod))
            df = pd.read_csv(file_name, index_col=0)
            # df["start_time"] = pd.to_datetime(df["start_time"], format="%Y%m%d %H:%M:%S.%f")
            df["sub_id"] = df["sub_id"].astype(str).str.zfill(2)
            # Add labels
            if _args.label_info != 'None':
                df_label_tmp = df_label[df_label["sub_id"] == sub_id]
                df_label_tmp = df_label_tmp.reset_index(drop=True)
            else:
                df_label_tmp = None
            add_label(df, df_label_tmp, mod, axis, sub_id, label_info=_args.label_info, debug=False)
            print(">> Success")


def handle_all_users(_args):
    # 
    # Main
    for _name in name_list[:]:
        sub_id = _name.split("_")[0]
        handle_single_user(_args, sub_id=sub_id)


# ------------------------------------------------------------------------
def main():
    parser = make_parser()
    args = parser.parse_args()
    print("Args:", args)
    args.func(args)


# ------------------------------------------------------------------------
if __name__=='__main__':
    main()
    

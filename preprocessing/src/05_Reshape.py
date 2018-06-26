# -----------------------------------------------------------------------
# Name: 05_reshape.py
# Author: Yoshimura Naoya
# Created: 2018.01.18
# Copyright:   (c) yoshimura 2017
#
# Purpose: Reshape labeled frames into DNN input style.
# -----------------------------------------------------------------------

import numpy as np
import pandas as pd
import argparse

""" Params
"""
sensor = "acc"
f_shape = (64, 1) # Shape of input DataFrame @100 Hz 
# Name list
name_list = [
    "01_kawabe",   "02_higashinaka", "03_yasuda", "04_kamiya",
    "05_ishiyama", "06_yoshimura",   "07_aiko",   "08_higashide",
    "09_others",   "10_others",      "11_others", "12_others",
    "13_others",   "14_others",      "15_others",
    "16_others", "17_others",
    "30_hada", "31_teramae","32_torisuke", "33_matsukawa","34_sato","35_hamase",
    "36_yamasaki","37_koguchi","38_onuma","39_kashiyama","40_yamaguchi",
    "41_watase","42_oga","43_shigeyoshi","44_hukuda","45_maekawa",
]


""" make parser
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
    single_parser.add_argument('--data-category',  required=True,
                               help='{gesture, object, none}')    
    single_parser.add_argument('--n',  required=True,
                             help='output shape (n, int)')

    

    # All
    all_parser = subparsers.add_parser('all')
    all_parser.set_defaults(func=handle_all_users)
    all_parser.add_argument('--data-category',  required=True,
                               help='{gesture, object, none}')    
    all_parser.add_argument('--n',  required=True,
                             help='output shape (n, int)')

    return parser



""" 
Main
"""
def handle_single_user(_args, sub_id=None):
    if not sub_id:
        _name = name_list[int(_args.user)-1]
        sub_id = _name.split("_")[0]
    print(">> sub_id={},".format(sub_id))
    # output sequence length
    n = int(_args.n)
    print(">> n = {}, _args.n={}".format(n, _args.n))
    print("")

    # Target columns on n64
    if int(sub_id) < 9:
        cols =  ['start_time', 'sub_id', 'label_id', 'session', 'mod', 'cat', 'label', 'no', 'axis',]
    else:
        cols =  ['start_time', 'sub_id', 'label_id', 'mod', 'cat', 'label', 'no', 'axis',]
    cols += ["x_{}".format(i+64) for i in range(-n,n,2)]
    cols += ["x_63"]
    print("[n64]")
    print("  columns={}\n".format(cols))
    # Names of new columns
    if int(sub_id) < 9:
        cols_new =  ['start_time', 'sub_id', 'label_id', 'session', 'mod', 'cat', 'label', 'no', 'axis',]
    else:
        cols_new =  ['start_time', 'sub_id', 'label_id', 'mod', 'cat', 'label', 'no', 'axis',]
    cols_new += ["x_{}".format(i) for i in range(0,n*2,2)]
    cols_new += ["true"]
    print("[n{}]".format(n))
    print("  columns={}\n".format(cols_new))    

    for mod in range(5):
        for axis in ["x", "y", "z"]:
            # Read CSV
            file_name = './dataStore/n64_{}/mg4_200Hz_sub{}_mod{}_{}_{}.csv'.format(
                    _args.data_category, sub_id, mod, sensor,axis)
            print("File name: ", file_name)
            df = pd.read_csv(file_name, index_col=0)
            df["sub_id"] = df["sub_id"].astype(str).str.zfill(2)
            # Select and Rename
            df_tmp = df[cols]
            df_tmp.columns = cols_new

            # Write CSV
            file_name_out = './dataStore/n{}s_{}/mg4_100Hz_sub{}_mod{}_{}_{}.csv'.format(
                n, _args.data_category, sub_id, mod, sensor, axis)
            df_tmp.to_csv(file_name_out, index=False)
            print(">> Success  : {}".format(file_name_out), df_tmp.shape)
    print(">> Done: mod={}\n\n".format(mod))


def handle_all_users(_args):
    for _name in name_list[:]:
        sub_id = _name.split("_")[0]
        handle_single_user(_args, sub_id)
                

# ------------------------------------------------------------------------
def main():
    parser = make_parser()
    args = parser.parse_args()
    print("Args:", args)
    args.func(args)


# ------------------------------------------------------------------------
if __name__=='__main__':
    main()
                    

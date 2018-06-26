# -----------------------------------------------------------------------
# Name: make_frame.py
# Author: Yoshimura Naoya
# Created: 2018.01.18
# Copyright:   (c) yoshimura 2017
#
# Purpose: make inputs frames from 200Hz sequence 
# -----------------------------------------------------------------------

import numpy as np
import pandas as pd


import argparse
import pandas as pd
import datetime as dt


""" Params
"""
sensor = "acc"
f_shape = (64, 1) # @100 Hz
root_dir = "./dataStore/n{}/".format(f_shape[0])
# name_list = [
#     "01_kawabe", "02_higashinaka", "03_yasuda", "04_kamiya",
#     "05_ishiyama", "06_yoshimura", "07_aiko", "08_higashide",
#     "09_others", "10_others", "11_others", "12_others",
#     "13_others", "14_others", "15_others",
#     "16_others", "17_others",
#     "30_hada", "31_teramae","32_torisuke", "33_matsukawa","34_sato","35_hamase",
#     "36_yamasaki","37_koguchi","38_onuma","39_kashiyama","40_yamaguchi",
#     "41_watase","42_oga","43_shigeyoshi","44_hukuda","45_maekawa",
# ]
name_list = [
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

    # All
    all_parser = subparsers.add_parser('all')
    all_parser.set_defaults(func=handle_all_users)

    return parser


""" Framing
"""
def framing_single_axis(df, sensor, mod, _name, root_dir, f_shape, debug=True):
    x,y,z = [], [], []
    for i in range(1,len(df)-f_shape[0]*2):
        time, sub_id, mod = df.loc[i+f_shape[0]-1, ["time", "sub_id", "mod"]]
        sub_id = str(sub_id).zfill(2)
        seq_x = list(df.loc[i:i+(f_shape[0]*2)-1, ["x"]].values.flatten())
        seq_y = list(df.loc[i:i+(f_shape[0]*2)-1, ["y"]].values.flatten())
        seq_z = list(df.loc[i:i+(f_shape[0]*2)-1, ["z"]].values.flatten())
        x.append([df.loc[i+f_shape[0]-1, "time"], sub_id, mod, "x",] + seq_x)
        y.append([df.loc[i+f_shape[0]-1, "time"], sub_id, mod, "y",] + seq_y)
        z.append([df.loc[i+f_shape[0]-1, "time"], sub_id, mod, "z",] + seq_z)
        if i%10000 == 0:
            print(">> Done: %d / %d (%f)"%(i, df.shape[0], i / df.shape[0]))
    df_x = pd.DataFrame(x, columns=["start_time", "sub_id", "mod", "axis",]+["x_{}".format(k) for k in range(f_shape[0]*2)])
    df_y = pd.DataFrame(y, columns=["start_time", "sub_id", "mod", "axis",]+["x_{}".format(k) for k in range(f_shape[0]*2)])
    df_z = pd.DataFrame(z, columns=["start_time", "sub_id", "mod", "axis",]+["x_{}".format(k) for k in range(f_shape[0]*2)])
    if not debug:
        file_name = root_dir + 'mg4_200Hz_sub{}_mod{}_{}_{}_framed.csv'
        df_x.to_csv(file_name.format(_name.split("_")[0], mod, sensor, "x"), index=True)
        df_y.to_csv(file_name.format(_name.split("_")[0], mod, sensor, "y"), index=True)
        df_z.to_csv(file_name.format(_name.split("_")[0], mod, sensor, "z"), index=True)
        print(">> Success: {} \n".format(file_name.format(_name.split("_")[0], mod, sensor, "3AXIS")))

        
def handle_single_user(_args):    
    # Select user
    _name = name_list[int(_args.user)-1]
    print("Selected User: ", _name)
    # Framing
    for mod in range(0,5):
        file_name = "./dataStore/DownSampled/mg4_200Hz_sub{}_mod{}_{}.csv".format(_name.split("_")[0], mod, sensor)
        df_HR = pd.read_csv(file_name)
        print("Start Framing: {}".format(file_name))
        print("df_HR.shape=", df_HR.shape)
        print("f_shape=", f_shape)
        framing_single_axis(df_HR, sensor, mod, _name, root_dir, f_shape, debug=False)



def handle_all_users(_args):
    # Params
    sensor = "acc"
    f_shape = (64, 1) # @100 Hz
    root_dir = "./dataStore/n{}/".format(f_shape[0])
    name_list = [
        "01_kawabe", "02_higashinaka", "03_yasuda", "04_kamiya",
        "05_ishiyama", "06_yoshimura", "07_aiko", "08_higashide",
    ]
    
    # Main
    for _name in name_list[:]:
        for mod in range(0,5):
            file_name = "./dataStore/DownSampled/mg4_200Hz_sub{}_mod{}_{}.csv".format(_name.split("_")[0], mod, sensor)
            df_HR = pd.read_csv(file_name)
            print("Start Framing: {}".format(file_name))
            print("df_HR.shape=", df_HR.shape)
            print("f_shape=", f_shape)
            framing_single_axis(df_HR, sensor, mod, _name, root_dir, f_shape, debug=False)


    
    

""" 
Main
"""
# ------------------------------------------------------------------------
def main():
    parser = make_parser()
    args = parser.parse_args()
    print("Args:", args)
    args.func(args)


# ------------------------------------------------------------------------
if __name__=='__main__':
    main()
    

            

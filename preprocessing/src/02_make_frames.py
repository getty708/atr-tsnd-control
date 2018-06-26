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

import const_params as ct



""" Params
"""
# sensor = "acc"
# f_shape = (64, 1) # @100 Hz


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
    parser.set_defaults(func=handle_single_user)
    parser.add_argument('--sub-id',  required=True,
                        help='a sub_id of the user(int)')
    parser.add_argument('--dir-root',  required=True,
                        help='a path to a root directory')
    return parser



""" Framing
"""
def framing_single_axis(df, sensor, mod, _name, root_dir, f_shape, debug=False):
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
        df_x.to_csv(file_name.format(ct.NAME_LIST["ID"], mod, sensor, "x"), index=True)
        df_y.to_csv(file_name.format(ct.NAME_LIST["ID"], mod, sensor, "y"), index=True)
        df_z.to_csv(file_name.format(ct.NAME_LIST["ID"], mod, sensor, "z"), index=True)
        print(">> Success: {} \n".format(file_name.format(ct.NAME_LIST["ID"], mod, sensor, "3AXIS")))
        

""" 
Main
"""
# ------------------------------------------------------------------------
def main():
    """ Params
    """
    # Argparse
    parser = make_parser()
    args = parser.parse_args()
    print("Args:", args)

    # Params
    sensor   = _args.sensor
    N        = _args.sensor
    DIR_ROOT = _args.dir_root
    f_shape = (N, 1) # @100 Hz

    """ Framing
    """
    # Select user
    name = ct.NAME_LIST[_args.user]
    print("Selected User: ", name["NAME"])
    # Framing
    for mod in range(0,5):
        file_name = "./dataStore/DownSampled/mg4_200Hz_sub{}_mod{}_{}.csv".format(name["ID"], mod, sensor)
        df_HR = pd.read_csv(file_name)
        print("Start Framing: {}".format(file_name))
        print("df_HR.shape=", df_HR.shape)
        print("f_shape=", f_shape)
        DIR_OUTPUT = ct.get_DIR(DIR_ROOT, N)
        framing_single_axis(df_HR, sensor, mod, _name, DIR_OUTPUT, f_shape, debug=False)
    


# ------------------------------------------------------------------------
if __name__=='__main__':
    main()
    

            

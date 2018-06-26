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

import const_params as ct

""" make parser
"""
def make_parser():
    """Initialize command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--sensor',  required=True,
                        help='seonsor type {acc, gyro}')
    parser.add_argument('--N',  required=True,
                        help='window size')
    parser.add_argument('--sub-id',  required=True,
                        help='a sub_id of the user(int)')
    parser.add_argument('--file-input',  required=True,
                        help='a path to a input file, e.g.: */n64/{mg4_200Hz_sub01_mod{mod}_{sensor}_{axis}.csv')    
    parser.add_argument('--file-output',  required=True,
                        help='a path to a output file, e.g.: */200Hz/{prefix}_200Hz_sub{}_mod{mod}_{sensor_{axis}.csv')    
    parser.add_argument('--data-category',  required=True,
                               help='{gesture, object, none}')
    parser.add_argument('--n',  required=True,
                        help='output shape (n, int)')
    return parser




# ------------------------------------------------------------------------
""" 
Main
"""
def main():
    parser = make_parser()
    args = parser.parse_args()
    print("Args:", args)

    # Params
    sensor      = args.sensor
    N           = int(args.N)
    sub_id      = args.sub_id
    user        = ct.NAME_LIST[args.sub_id]
    file_input  = args.file_input
    file_output = args.file_output
    f_shape = (N, 1) # @100 Hz

    
    # Main
    print(">> sub_id={},".format(sub_id))
    # output sequence length
    n = int(args.n)
    print(">> n = {}, args.n={}".format(n, args.n))
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
            filename = file_input.format(mod=mod, sensor=sensor, axis=axis)
            print("File name: ", file_name)
            df = pd.read_csv(file_name, index_col=0)
            df["sub_id"] = df["sub_id"].astype(str).str.zfill(2)
            # Select and Rename
            df_tmp = df[cols]
            df_tmp.columns = cols_new

            # Write CSV
            filename = file_output.format(mod=mod, sensor=sensor, axis=axis)            
            df_tmp.to_csv(filename, index=False)
            print(">> >> Done: {}".format(filename), df_tmp.shape)
        print(">> Done: mod={}\n\n".format(mod))
    print(">> Success\n\n")

    
# ------------------------------------------------------------------------
if __name__=='__main__':
    main()
                    

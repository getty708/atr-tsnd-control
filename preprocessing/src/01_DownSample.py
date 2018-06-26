# -----------------------------------------------------------------------
# Name: 01_down_sampling.py
# Author: Yoshimura Naoya
# Created: 2018.06.26
# Copyright:   (c) yoshimura 2018
#
# Purpose: make inputs frames from 200Hz sequence 
# -----------------------------------------------------------------------

import os
import argparse
import numpy as np
import pandas as pd
import datetime as dt

import const_params as ct


""" make parser
"""
def make_parser():
    """Initialize command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-input',  required=True,
                        help='a path to a input file (*/{}_1000Hz_sub{}_mix.csv)')
    parser.add_argument('--file-output',  required=True,
                        help='a path to a output file (*/{prefix}_{fs}Hz_sub{ID}_mix.csv)')
    parser.add_argument('--seq-type',  required=True,
                        help='Key of sequence config {e.g. 1000Hz, 200Hz}')
    return parser




# ---------------------------------------------------------------------------------
# =======================================
#  Downaample: Filters for downsampling
# =======================================
def filter_by_timestamp(df_seq, m=0, step=1):
    """ Select rows based on timestamp
    
    Args.
    -----
    - df_seq : pd.DataFrame, Column `time` is necessary
    - m      : integer,  Start of interval.
    
    Return.
    -------
    - pd.DataFrame
    """
    # Check input
    assert isinstance(df_seq, pd.DataFrame), "Error: df_seq must be pd.DataFrame [your input={}]".format(type(df_seq))
    assert "time" in df_seq.columns, "Error: Input DataFrame must have a column named as `time`"
    assert isinstance(df_seq.loc[0, "time"], dt.datetime), "Error: Date Type of column[`time`] must be dt.datetime"
    
    # Downsampling
    df = df_seq[["time"]].copy()
    df["ms"] = df["time"].dt.microsecond / 1000.
    df["selected"] = df["ms"].apply(lambda ms: True if ms%step == 0 else False)
    # return df[df["selected"] == True].reset_index(drop=True)
    return df_seq[df["selected"]].reset_index(drop=True)



# ==================
#  Downaample: Main
# ==================
def apply_downsampling(seq, step, filter_global=False, filter_local=False, **kwargs):
    """ Apply Down Samplings
    Args.
    -----
    - seq  : list [e.g. np.ndarray(), pd.DataFrame]
    - step : integer, Spaceing between values
    
    Return.
    -------
    - lsit of donwsampled `seq`
    """
    seq_list = []
    # Apply filters [whole sequence]
    if not isinstance(filter_global, bool):
        seq = filter_global(seq, **kwargs)
    for start in range(step):
        if not isinstance(filter_local, bool):
            # Apply local filter
            seq_new = filter_local(seq, start, step=step, **kwargs)
        else:
            seq_new = seq[start::step]
        seq_list.append(seq_new)
    return seq_list    


# ---------------------------------------------------------------------------------
""" 
Main
"""
if __name__=='__main__':
    """ Params
    """
    # Argparse
    parser = make_parser()
    args = parser.parse_args()
    print("Args:", args)

    # Params
    seq_type = ct.SEQ_CONFIG[args.seq_type]
    fs, step = seq_type["fs"], seq_type["step"]
    file_input  = args.file_input
    file_output = args.file_output
    
    #
    # Main Op
    #
    print("File Imput: {}".format(file_input))
    print(">> seq_type={}".format(seq_type))
    print(">> fs={}, step={}".format(fs, step))
    df = pd.read_csv(file_input, index_col=0)
    df["time"] = pd.to_datetime(df["time"])
    print(df.head())

    
    # Downsampling
    df_list = apply_downsampling(df, step=step, filter_local=filter_by_timestamp,)
    

    # Write
    for mod, df_tmp in enumerate(df_list):
        filename = file_output.format(mod=mod)
        df_tmp.to_csv(filename, index=False)
        print(">> Done: mod={}, filename={}".format(mod, filename))
    print(">> Success\n\n")

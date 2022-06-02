import os
import sys
import subprocess
import shutil
import argparse
from zipfile import ZipFile
import pandas as pd
import numpy as np

def make_parser():
    parser = argparse.ArgumentParser(
        description="Convert ATR log file into multiple .csv files for ADL Tagger"
    )
    # Add Arguments
    parser.add_argument('--path-to-raw', required=True,
                        help="A path to main folder containing raw data from required users, e.g.{G:\\User\\xxx\\open-pack\data\raw}")
    parser.add_argument('--path-output', required=True,
                        help="A path to main folder for output files, e.g.{G:\\User\\xxx\\open-pack\data\ADLTagger}")
    parser.add_argument('--path-to-shifts', required=True,
                        help="A path to device shift .csv file. {PATH\\wearable_shifts.csv}")
    parser.add_argument('--users', default = 'all',
                        help="list of Users to be extracted. {[U0101,U0102], all}")
    parser.add_argument('--devices', default = 'all',
                        help="list of devices to be extracted. {[atr01,atr02], all}")
    parser.add_argument('--unit', default='g',
                        help="Acc unit to convert to, {g, m/s2}")
    return parser

def main():
    # Parse Command Line Argumenmts
    parser = make_parser()
    args = parser.parse_args()

    #Assign comand line arguments to variable
    main_folder = args.path_to_raw
    output_main = args.path_output
    shifts_path = args.path_to_shifts

    #Check user and device availability
    shifts_df = pd.read_csv(shifts_path)
    shifts_df['av_user'] = shifts_df.duplicated(['user'],keep='first')
    available_users = list(shifts_df[shifts_df['av_user']==False]['user'])
    #print(available_users)

    if args.users == 'all':
        users_l = available_users
    else:
        users_l = args.users.split(',')

    if args.devices == 'all':
        devices_l = ['atr01','atr02','atr03','atr04']
    else:
        devices_l = args.devices.split(',')

    for user in users_l:
        if user not in available_users:
            sys.exit("User {} not available in shifts.csv file".format(user))

    for device in devices_l:
        if device not in ['atr01','atr02','atr03','atr04']:
            sys.exit("Device {} not valid".format(device))

    #Run log_to_adl.py by user/device & session

    for user in users_l:

        sessions_l = list(shifts_df[shifts_df['user']==user]['session'])
        date = str(list(shifts_df[shifts_df['user']==user]['date'])[0])
        sensor = str(list(shifts_df[shifts_df['user']==user]['atr_type'])[0])
        print('sensor:', sensor)
        work_df = pd.DataFrame(shifts_df[shifts_df['user']==user])

        for device in devices_l:
            for session in sessions_l:
                path_to_log = os.path.join(main_folder,date+'_'+user,device, session + '.log')
                path_output_dir = os.path.join(output_main,user,device,session)
                shift = str(list(work_df[work_df['session']==session][device+'_shift'])[0])

                print("python log_to_adl.py " + ("--path-input-log "+path_to_log) + (" --path-output-dir "+path_output_dir) + (" --date "+ date[:4]+'-'+date[4:6]+'-'+date[-2:]) + (" --shift "+shift ) + (" --unit "+ args.unit) + 
                      (" --sensor "+ sensor))

                subprocess.run("python log_to_adl.py " + ("--path-input-log "+path_to_log) + (" --path-output-dir "+path_output_dir) + (" --date "+ date[:4]+'-'+date[4:6]+'-'+date[-2:]) + (" --shift "+shift ) + (" --unit "+ args.unit) + 
                      (" --sensor "+ sensor))

        
if __name__=='__main__':
    main()
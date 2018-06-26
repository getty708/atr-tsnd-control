#
# Preporcessing for No label data
#
user_id=$1;
frame_size=64;

if [ ${user_id} > 17];
then
    user_idx=$((${user_id}-12));
else
    user_idx=${user_id};
fi

# echo "";
# echo Start;
# echo user_id = ${user_id}, [user_idx =  ${user_idx}];
# echo frame_size: ${frame_size}

## Step.2 Framing
#python 02_make_frames.py            single --user ${user_idx}
# Step.3 Add label info
#python 03_add_label.py              single --user ${user_idx}
# Step.4 Split by cat
#python 04_split_by_data_category.py single --user ${user_idx} --data-category none
# Step.5 Reshape
echo "";
echo Start;
echo user_id  =  ${user_id};
echo user_idx =  ${user_idx};
echo frame_size: ${frame_size}
python 05_Reshape.py                single --user ${user_idx} --data-category none --n ${frame_size}
#for user_idx in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33
# for user_idx in 45
# do
#     echo "";
#     echo Start;
#     echo user_idx =  ${user_idx};
#     echo frame_size: ${frame_size}
#     python 05_Reshape.py                single --user ${user_idx} --data-category none --n ${frame_size}
# done

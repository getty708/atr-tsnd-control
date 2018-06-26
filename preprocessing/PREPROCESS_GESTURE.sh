#
# Preporcessing for No label data
#
user_idx=$1;
frame_size=8;



#user_idx=$((${user_id}-29));
echo user_id = ${user_id}, [user_idx =  ${user_idx}];
echo frame_size: ${frame_size}

# Step.2 Framing
# python 02_make_frames.py            single --user ${user_idx}
# # Step.3 Add label info
# python 03_add_label.py              single --user ${user_idx} --label-info ./dataStore/label_info2.csv
# # Step.4 Split by cat
# python 04_split_by_data_category.py single --user ${user_idx} --data-category none
# Step.5 Reshape
# python 05_Reshape.py                single --user ${user_idx} --data-category none --n ${frame_size}

#
# Split Gesture
#
# Step.4 Split by cat
# python 04_split_by_data_category.py single --user ${user_idx} --data-category gesture
# Step.5 Reshape
python 05_Reshape.py                single --user ${user_idx} --data-category gesture --n ${frame_size}

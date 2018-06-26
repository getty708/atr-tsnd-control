#
# Preporcessing for No label data
#
sub_id=$1;
frame_size=64;
sensor="gyro"
DIR_ROOT="/home/dragon/yoshimura/dataStoreRoot/2018_01_16/dataStore"

echo "";
echo Start;
echo sub_id    : ${user_id};
echo frame_size: ${frame_size};

# Step.2 Framing
# python ./src/02_make_frames.py \
#     --sensor       ${sensor} \
#     --N            ${frame_size} \
#     --sub-id       ${sub_id} \
#     --file-input   /home/dragon/yoshimura/dataStoreRoot/2018_01_16/dataStore/200Hz/mg4_200Hz_sub${sub_id}_mod{mod}_mix.csv \
#     --file-output  /home/dragon/yoshimura/dataStoreRoot/2018_01_16/dataStore/n64/mg4_200Hz_sub${sub_id}_mod{mod}_{sensor}_{axis}.csv

# Step.3 Add label info
python ./src/03_add_label.py \
    --sensor       ${sensor} \
    --N            ${frame_size} \
    --sub-id       ${sub_id} \
    --file-input   ${DIR_ROOT}/n64/mg4_200Hz_sub${sub_id}_mod{mod}_{sensor}_{axis}.csv \
    --file-output  ${DIR_ROOT}/n64_labeled/mg4_200Hz_sub${sub_id}_mod{mod}_{sensor}_{axis}.csv \
    --label-info   None


# Step.4 Split by cat
python ./src/04_split_by_data_category.py \
       --sensor       ${sensor} \
       --N            ${frame_size} \
       --sub-id       ${sub_id} \
       --file-input   ${DIR_ROOT}/n64_labeled/mg4_200Hz_sub${sub_id}_mod{mod}_{sensor}_{axis}.csv \
       --file-output  ${DIR_ROOT}/n64_none/mg4_200Hz_sub${sub_id}_mod{mod}_{sensor}_{axis}.csv \
       --data-category none


# Step.5 Reshape
python ./src/05_reshape.py \
       --sensor       ${sensor} \
       --N            ${frame_size} \
       --sub-id       ${sub_id} \
       --file-input   ${DIR_ROOT}/n64_noe/mg4_200Hz_sub${sub_id}_mod{mod}_{sensor}_{axis}.csv \
       --file-output  ${DIR_ROOT}/n64s_none/mg4_200Hz_sub${sub_id}_mod{mod}_{sensor}_{axis}.csv \
       --data-category none \
       --n            ${frame_size}

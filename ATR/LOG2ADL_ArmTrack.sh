# 2018.08.03
root_dir="2018_07_17"
date="2018-07-17"
array_id="01 02 03 04"

# # 2018.08.03
# root_dir="2018_08_03"
# date="2018-08-03"
# array_id="10 11 12 13 14 15"


for sub_id in ${array_id};
do
    # Params
    echo Params: ${sub_id}
    # Exe
    python ./src/log_to_adl.py \
    	   --path-input-log   /root/dataStore_upconversion/data/${root_dir}/LOG/arm${sub_id}.log \
    	   --date             ${date} \
    	   --shift            0.0 \
    	   --path-output-dir  /root/dataStore_upconversion/data/${root_dir}/ADL/ADL_arm${sub_id}/ 
done

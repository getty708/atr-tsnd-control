root_dir="2018_01_16"
date="2018-01-16"
sub_id="03"
sub_name="yasuda"
echo Params: ${sub_id} ${sub_name}



python ./src/log_to_adl.py \
       --path-input-log   /root/dataStore_upconversion/data/${root_dir}/${sub_id}_${sub_name}/data/log/${sub_id}_${sub_name}.log \
       --date             ${date} \
       --shift            0.0 \
       --path-output-dir  /root/dataStore_upconversion/data/${root_dir}/CSV/ADL/ADL_${sub_id}_${sub_name}/ 

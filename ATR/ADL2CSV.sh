root_dir="2018_01_16"
sub_id="02"
sub_name="higashinaka"
prefix="mg3"


python ./src/adl_to_csv.py MIX \
       --path-input-root-dir-acc   /root/dataStore_upconversion/data/${root_dir}/${sub_id}_${sub_name}/data/acc2 \
       --path-input-root-dir-gyro  /root/dataStore_upconversion/data/${root_dir}/CSV/ADL/ADL_${sub_id}_${sub_name}/Gryo \
       --path-input-xml            /root/dataStore_upconversion/data/${root_dir}/${sub_id}_${sub_name}/data.xml \
       --path-output-dir           /root/dataStore_upconversion/data/${root_dir}/CSV/ \
       --filename-csv              ${prefix}_1000Hz_sub${sub_id}_mix.csv \
       --filename-label            ${prefix}_sub${sub_id}_label_detail.csv \
       --filename-summary          ${prefix}_sub${sub_id}_label_summary.csv

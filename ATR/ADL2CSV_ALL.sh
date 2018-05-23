root_dir="2018_01_16"
date="2018-01-16"
prefix="mg3"

array_id=(01 02 03 04 05 06 07 08)
array_name=("kawabe" "higashinaka" "yasuda" "kamiya" "ishiyama" "yoshimyura" "aiko" "higashide")
N=8

for idx in `seq 0 $((${N}-1))`;
do
    # Params
    sub_id=${array_id[${idx}]}
    sub_name=${array_name[${idx}]}
    echo Params: ${idx} ${sub_id} ${sub_name}
    # Exec
    python ./src/adl_to_csv.py MIX \
	   --path-input-root-dir-acc   /root/dataStore_upconversion/data/${root_dir}/${sub_id}_${sub_name}/data/acc2 \
	   --path-input-root-dir-gyro  /root/dataStore_upconversion/data/${root_dir}/CSV/ADL/ADL_${sub_id}_${sub_name}/Gryo \
	   --path-input-xml            /root/dataStore_upconversion/data/${root_dir}/${sub_id}_${sub_name}/data.xml \
	   --path-output-dir           /root/dataStore_upconversion/data/${root_dir}/CSV/ \
	   --filename-csv              ${prefix}_1000Hz_sub${sub_id}_mix.csv \
	   --filename-label            ${prefix}_sub${sub_id}_label_detail.csv \
	   --filename-summary          ${prefix}_sub${sub_id}_label_summary.csv
done

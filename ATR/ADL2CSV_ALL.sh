root_dir="2017_12_15"
date="2017-12-15"
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
	   --path-input-root-dir-gyro  /root/dataStore_upconversion/data/${root_dir}/CSV/ADL/ADL_${sub_id}_${sub_name}/Gyro \
	   --path-input-xml            /root/dataStore_upconversion/data/${root_dir}/${sub_id}_${sub_name}/data.xml \
	   --path-output-dir           /root/dataStore_upconversion/data/${root_dir}/CSV/ \
	   --filename-csv              ${prefix}${sub_id}_ags.csv \
	   --filename-label            None \
	   --filename-summary          None
	   # --filename-label            ${prefix}_sub${sub_id}_label_detail.csv \
	   # --filename-summary          ${prefix}_sub${sub_id}_label_summary.csv
done



# # No Label
# array_id=(10 11 12 13 14 15 16 17 31 34 36 37 40 41 42 43 45)
# array_name=("others" "others" "others" "others" "others" "others" "others" "others" "teramae" "sato" "yamasaki" "koguchi" "yamaguchi" "watase" "oga" "shigeyoshi" "maekawa") 
# N=17

# for idx in `seq 0 $((${N}-1))`;
# do
#     # Params
#     sub_id=${array_id[${idx}]}
#     sub_name=${array_name[${idx}]}
#     echo Params: ${idx} ${sub_id} ${sub_name}
#     # Exec
#     python ./src/adl_to_csv.py MIX \
# 	   --path-input-root-dir-acc   /root/dataStore_upconversion/data/${root_dir}/${sub_id}_${sub_name}/data/acc2 \
# 	   --path-input-root-dir-gyro  /root/dataStore_upconversion/data/${root_dir}/CSV/ADL/ADL_${sub_id}_${sub_name}/Gyro \
# 	   --path-input-xml            None \
# 	   --path-output-dir           /root/dataStore_upconversion/data/${root_dir}/CSV/ \
# 	   --filename-csv              ${prefix}${sub_id}_ags.csv \
# 	   --filename-label            None \
# 	   --filename-summary          None
# done



# # labeled Data
# array_id=(30 32 33 35 38 39 44)
# array_name=("hada" "torisuke" "matsukawa" "hamase" "onuma" "kashiyama" "hukuda")
# N=7

# for idx in `seq 0 $((${N}-1))`;
# do
#     # Params
#     sub_id=${array_id[${idx}]}
#     sub_name=${array_name[${idx}]}
#     echo Params: ${idx} ${sub_id} ${sub_name}
#     # Exec
#     python ./src/adl_to_csv.py MIX \
# 	   --path-input-root-dir-acc   /root/dataStore_upconversion/data/${root_dir}/${sub_id}_${sub_name}/data/acc2 \
# 	   --path-input-root-dir-gyro  /root/dataStore_upconversion/data/${root_dir}/CSV/ADL/ADL_${sub_id}_${sub_name}/Gyro \
# 	   --path-input-xml            /root/dataStore_upconversion/data/${root_dir}/${sub_id}_${sub_name}/data.xml \
# 	   --path-output-dir           /root/dataStore_upconversion/data/${root_dir}/CSV/ \
# 	   --filename-csv              ${prefix}${sub_id}_ags.csv \
# 	   --filename-label            None \
# 	   --filename-summary          None
# 	   # --filename-label            ${prefix}_sub${sub_id}_label_detail.csv \
# 	   # --filename-summary          ${prefix}_sub${sub_id}_label_summary.csv
# done


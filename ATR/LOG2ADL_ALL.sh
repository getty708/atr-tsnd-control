root_dir="2017_12_15"
date="2017-12-15"

# # Labeled #1
# array_id=(01 02 03 04 05 06 07 08)
# array_name=("kawabe" "higashinaka" "yasuda" "kamiya" "ishiyama" "yoshimura" "aiko" "higashide")
# N=8


# # Labeled #2
# array_id=(30 32 33 35 38 39 44)
# array_name=("hada" "torisuke" "matsukawa" "hamase" "onuma" "kashiyama" "hukuda")
# N=7 

# # no Label
# array_id=(10 11 12 13 14 15 16 17 31 34 36 37 40 41 42 43 45)
# array_name=("others" "others" "others" "others" "others" "others" "others" "others" "teramae" "sato" "yamasaki" "koguchi" "yamaguchi" "watase" "oga" "shigeyoshi" "maekawa") 
# N=17



for idx in `seq 0 $((${N}-1))`;
do
    # Params
    sub_id=${array_id[${idx}]}
    sub_name=${array_name[${idx}]}
    echo Params: ${idx} ${sub_id} ${sub_name}
    # Exe
    python ./src/log_to_adl.py \
    	   --path-input-log   /root/dataStore_upconversion/data/${root_dir}/${sub_id}_${sub_name}/data/log/${sub_id}_${sub_name}.log \
    	   --date             ${date} \
    	   --shift            0.0 \
    	   --path-output-dir  /root/dataStore_upconversion/data/${root_dir}/CSV/ADL/ADL_${sub_id}_${sub_name}/ 
done

root_dir="2018_08_03"
date="2018-08-03"
prefix="arm"

# Labeled #1
# id_list="09 10 11 12 13" # 2018.01.16
# id_list="14" # 2018.01.18
# id_list="15" # 2018.01.19
# id_list="16" # 2018.01.20
# id_list="17" # 2018.01.22
# id_list="31 34" # 2018.01.31
# id_list="36 37" # 2018.02.01
# id_list="40 41 42 43" # 2018.02.03
# id_list="45" # 2018.02.04

# id_list="01 02 03 04"
# sensor="geo"
id_list="10 11 12 13 14 15"
sensor="ags"




for id in ${id_list};
do
    # Params
    echo Params: prefix = ${prefix}, id =  ${id}, root = ${root}, date = ${date} 
    # Exe
    python ./src/log_to_csv.py \
	   --sensor           ${sensor} \
    	   --filename-input   /root/dataStore_upconversion/data/${root_dir}/LOG/${prefix}${id}.log \
	   --filename-output  /root/dataStore_upconversion/data/${root_dir}/CSV/${prefix}${id}_${sensor}.csv \
    	   --date             ${date} \
    	   --shift            0.0 
done

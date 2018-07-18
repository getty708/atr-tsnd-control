root_dir="2018_07_17"
date="2018-07-17"
prefix="arm"

# Labeled #1
id_list="01 02 04"
sensor="geo"



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

#sub_id_list="01 02 03 04 05 06 07 08 10 11 12 13 14 15 16 17 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45"
sub_id_list=06
fs=200


for sub_id in ${sub_id_list};
do
    echo sub_id: ${sub_id}
    python ./src/01_DownSample.py \
	   --file-input   /root/dataStore_upconversion/data/2018_01_16/CSV/mg4_1000Hz_sub${sub_id}_mix.csv \
	   --file-output  /root/dataStore_upconversion/data/2018_01_16/dataStore/200Hz/mg4_${fs}Hz_sub${sub_id}_mod{mod}_mix.csv \
	   --seq-type     ${fs}Hz
done

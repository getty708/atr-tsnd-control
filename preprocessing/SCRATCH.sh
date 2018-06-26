#sub_id_list="01 02 03 04 05 06 07 08 30 32 33 35 38 39 44"
sub_id_list="10 11 12 13 14 15 16 17 31 34 36 37 40 41 42 43 45"


for sub_id in ${sub_id_list};
do
    bash PREPROCESS_NONE.sh ${sub_id}
done

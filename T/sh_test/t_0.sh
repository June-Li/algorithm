file_list=$(ls /Volumes/my_disk/company/sensedeal/PycharmProject/test/)

time=$(date "+%Y-%m-%d %H:%M:%S")
echo "\n\n\n\n\n**************************  $time  **************************" >> t_0.log
for dir in $file_list
do
#  python t_10.py
  echo $dir
  echo $dir >> t_0.log
done

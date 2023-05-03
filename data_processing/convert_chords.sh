# this script converts the from a file into the expanded version

for file in ../RAW_DATA/rs200_harmony/*.har;

do 
    # cat "${file%.html}.txt"
    ./expand6 -v 3 $file > "${file%.har}.txt"
done
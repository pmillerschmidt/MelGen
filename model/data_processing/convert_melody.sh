# this script converts the from a file into the expanded version

for file in ../RAW_DATA/rs200_melody/*.mel;

do 
    # cat "${file%.html}.txt"
    ./process-mel5.pl 3 0 $file > "${file%.mel}.txt"
done
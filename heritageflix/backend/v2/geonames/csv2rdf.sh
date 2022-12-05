#!/bin/bash

set -e

currentDir=$(cd $(dirname $0) && pwd -P)
configDir="$currentDir/config"
dataDir="$currentDir/data"
tmpDir="$currentDir/tmp"

tarql=$currentDir/tarql-1.2/bin/tarql
if [! [ -f $tarql && -x $tarql ]]; then
  echo "Cannot execute Tarql: $tarql"
  exit 1
fi

# Remove the old files, if any
rm -rf $dataDir
mkdir -p $dataDir

rm -rf $tmpDir
mkdir -p $tmpDir

cd $tmpDir

# For future improvement:
# cp $configDir/headers-admin1-codes.txt $dataDir/admin1-codes.txt
# curl -O "https://download.geonames.org/export/dump/admin1CodesASCII.txt"
# cat admin1CodesASCII.txt >> $dataDir/admin1-codes.txt

cp $configDir/headers-gn.txt NL01.txt
curl -O "https://download.geonames.org/export/dump/NL.zip"
unzip "NL.zip"
cat NL.txt >> NL01.txt

# Add column with admin code (= countryCode + admin1Code)
awk 'BEGIN{FS=OFS="\t"} {print $0, (NR>1 ? $9"."$11 : "admin1GeonamesId")}' NL01.txt > NL02.txt

# Replace admin code with GeoNames ID, according to (https://download.geonames.org/export/dump/admin1CodesASCII.txt):
# NL.01	Drenthe	Drenthe	2756631
# NL.02	Friesland	Friesland	2755812
# NL.03	Gelderland	Gelderland	2755634
# NL.04	Groningen	Groningen	2755249
# NL.05	Limburg	Limburg	2751596
# NL.06	North Brabant	North Brabant	2749990
# NL.07	North Holland	North Holland	2749879
# NL.09	Utrecht	Utrecht	2745909
# NL.10	Zeeland	Zeeland	2744011
# NL.11	South Holland	South Holland	2743698
# NL.15	Overijssel	Overijssel	2748838
# NL.16	Flevoland	Flevoland	3319179
awk -F '\t' -v OFS='\t' \
  '$20 == "NL.01" { $20 = "2756631" }; $20 == "NL.02" { $20 = "2755812" }; $20 == "NL.03" { $20 = "2755634" }; $20 == "NL.04" { $20 = "2755249" }; $20 == "NL.05" { $20 = "2751596" }; $20 == "NL.06" { $20 = "2749990" }; $20 == "NL.07" { $20 = "2749879" }; $20 == "NL.09" { $20 = "2745909" }; $20 == "NL.10" { $20 = "2744011" }; $20 == "NL.11" { $20 = "2743698" }; $20 == "NL.15" { $20 = "2748838" }; $20 == "NL.16" { $20 = "3319179" }1' \
  NL02.txt > NL03.txt

cd $currentDir

$tarql -t $currentDir/locations.rq $tmpDir/NL03.txt > $dataDir/locations.ttl

rm -rf $tmpDir

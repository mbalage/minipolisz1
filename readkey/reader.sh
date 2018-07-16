mkdir /tmp/rfids/
while read line
do
  touch "/tmp/rfids/$line"
  wget -qO-  http://www.mbd.hu/fundamenta/storeCoin.php?rfid=$line &> /tmp/last_coin_store 
  echo "$line"
done < "${1:-/dev/stdin}"


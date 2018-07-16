mkdir /tmp/rfids/
while read line
do
  touch "/tmp/rfids/$line"
  wget "http://www.mbd.hu/fundamenta/storeCoin.php?rfid=$line" > /tmp/last_coin_store 2>&1  &
  echo "$line"
done < "${1:-/dev/stdin}"


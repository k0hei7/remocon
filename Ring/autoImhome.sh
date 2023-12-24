now=`date +%H%M`
if [ 0000 -le $now -a 0530 -ge $now -o 1030 -le $now -a 2359 -ge $now ]; then
  /home/pi/Documents/HomeSiri/Light.sh
  /home/pi/Documents/HomeSiri/Aircon.sh
  python /home/pi/git/remocon/IR-remo222.py tf /home/pi/git/remocon/TV_onoff
fi

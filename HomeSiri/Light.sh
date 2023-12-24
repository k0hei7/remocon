tmp=`head -n 1 /home/pi/Documents/HomeSiri/Light | tail -n 1`
var=`echo $tmp`

case "$var" in
  "off" ) /home/pi/Documents/HomeSiri/Light_off.sh
        sed -i "1 s/off/on/g" /home/pi/Documents/HomeSiri/Light;;

  "on" ) /home/pi/Documents/HomeSiri/Light_on.sh
        sed -i "1 s/on/off/g" /home/pi/Documents/HomeSiri/Light;;

esac

tmp=`head -n 1 /home/pi/Documents/HomeSiri/Aircon | tail -n 1`
var=`echo $tmp`

case "$var" in
  "off" ) /home/pi/Documents/HomeSiri/Aircon_off.sh
        sed -i "1 s/off/on/g" /home/pi/Documents/HomeSiri/Aircon;;

  "on" ) /home/pi/Documents/HomeSiri/Aircon_on.sh
        sed -i "1 s/on/off/g" /home/pi/Documents/HomeSiri/Aircon;;

esac

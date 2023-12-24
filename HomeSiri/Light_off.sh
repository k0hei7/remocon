#python /home/pi/git/python-host/switchbot.py E5:CF:94:48:74:E8 Press
python /home/pi/git/remocon/IR-remo222.py tf /home/pi/git/remocon/Bedlight_off
python /home/pi/git/remocon/IR-remo222.py tf /home/pi/git/remocon/Bedlight_on
sed -i "3 s/true/false/g" /home/pi/Documents/HomeSiri/State/StateMemo.txt

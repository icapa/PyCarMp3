#/bin/bash
sudo python /home/pi/PyCarMp3/player.py > /dev/null &
sleep 2
sudo python /home/pi/PyCarMp3/ui.py > /dev/null &

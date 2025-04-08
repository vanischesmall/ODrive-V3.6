sudo apt install python3 python3-pip
pip3 install --upgrade odrive
sudo bash -c "curl https://cdn.odriverobotics.com/files/odrive-udev-rules.rules > /etc/udev/rules.d/91-odrive.rules && udevadm control --reload-rules && udevadm trigger"

echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc 

sudo usermod -a -G dialout $USER


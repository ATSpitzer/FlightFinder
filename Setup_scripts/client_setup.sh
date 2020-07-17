sudo apt update
sudo apt install python3-pip -y
sudo apt install firefox -y
sudo apt install shadowsocks-libev -y

pip3 install selenium
pip3 install pandas

cd ~
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar -xvzf geckodriver-v0.26.0-linux64.tar
chmod +x geckodriver
sudo ln -s ~/geckodriver /usr/bin/geckodriver

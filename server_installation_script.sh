#
# Clone git repo
#
sudo apt-get update
sudo apt-get install python-pip -y
sudo pip install git+https://github.com/shadowsocks/shadowsocks.git@master

sudo apt install software-properties-common -y
sudo add-apt-repository ppa:max-c-lv/shadowsocks-libev -y
sudo apt update -y
sudo apt install shadowsocks-libev -y


#Create /etc/ssConfig.json
sudo ssserver -c /etc/ssConfig.json -d start



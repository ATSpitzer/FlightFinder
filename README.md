# FlightFinder
There is a reported phenomenon where hotel and flight prices (among other things) differ when using a vpn to appear to be in a different country.
This is a project to automate a search for hotels, perform that search iterating through VPNs in different countries, and generate a report concerning the prices returned--highlighting any differences.

## Setup
To run this application you must set up VPN servers and a client machine to connect to them.

#### Server
Run the setup script and the python script to generate config files and start VPN server
```
./FlightFinder/Setup_scripts/server_setup.sh
sudo python3 FlightFinder/Vpn_Tool/VpnServer.py
```

#### Client
Run the setup script for the client machine
```
./FlightFinder/Setup_scripts/client_setup.sh
```

Then for each server you have setup, run the following to create a corresponding config file
```
sudo python3 FlightFinder/Vpn_Tool/VpnTool.py add_server -c <country name> -a <public ip address of server>
```

## Example
Here is the output of `scripts/link_us_india.py` having setup VPN servers in India and the United States

```
ubuntu@client-1:~/FlightFinder/scripts$ python3 link_us_india.py 
Link: https://us.trip.com/hotels/list?city=810&countryId=0&checkin=2020/08/13&checkout=2020/08/14&optionId=810&opti
onType=City&directSearch=1&optionName=cinnamon%20garden&display=Colombo&crn=1&adult=1&children=0&searchBoxArg=t&tra
velPurpose=0&ctm_ref=ix_sb_dl&domestic=1
Results:
---------------------------------
                                   usa india
Colombo Villa at Cambridge Place   $80   $80
The Rosmead                       $105  $105
Yoho Rooms @ The Irish             $56   $56
Fern Colombo                       $54   $54
Paradise Road Tintagel Colombo    $238  $254
Maniumpathy Hotel                 $213  $205
Rockwell Colombo                   $43   $43
Zylan Luxury Villa                 $69  $102
Golf Link Colombo                  $60   $60
Groove House                       $11   $11
```

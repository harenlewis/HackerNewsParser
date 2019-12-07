#/bin/bash

echo "Setting up the project and downloading dependencies....."

sudo apt-get update
sudo apt-get install acl -y

sudo apt-get install python3.5-dev -y
sudo apt-get install python-pip

pip install -r requirements.txt

sudo python3 stories_processor.py

echo "Compeleted parsing. Please check csv files for parsed data in the same directory."

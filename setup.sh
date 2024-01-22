# /bin/bash

# Python
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# RCB4Lib
mkdir -p lib
cd lib
curl -O https://kondo-robot.com/w/wp-content/uploads/RCB4Lib_for_Python_V100B.zip
unzip RCB4Lib_for_Python_V100B.zip
cp -r RCB4Lib_for_Python_V100B/Rcb4Lib/* .
rm -rf RCB4Lib_for_Python_V100B
rm RCB4Lib_for_Python_V100B.zip
cd ..

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
black Rcb4BaseLib.py # インデントに tab が混ざっているのを修正
sed -i 's/return 0, Rcb4BaseLib.CmdOkType.Error.value, buf/return 0, Rcb4BaseLib.CmdOkType.Error.value, txbuf/' Rcb4BaseLib.py # 変数名のミスを修正
cd ..

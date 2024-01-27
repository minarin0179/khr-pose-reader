# /bin/bash

# Python
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# RCB4Lib
mkdir -p lib
curl -o lib/RCB4Lib.zip https://kondo-robot.com/w/wp-content/uploads/RCB4Lib_for_Python_V100B.zip
unzip lib/RCB4Lib.zip -d lib && rm lib/RCB4Lib.zip
cp -r lib/RCB4Lib_for_Python_V100B/Rcb4Lib/Rcb4BaseLib.py lib/Rcb4BaseLib/ && rm -rf lib/RCB4Lib_for_Python_V100B

# RCB4Lib の修正
black lib/Rcb4BaseLib/Rcb4BaseLib.py # インデントに含まれる Tab を Space に修正
sed -i 's/return 0, Rcb4BaseLib.CmdOkType.Error.value, buf/return 0, Rcb4BaseLib.CmdOkType.Error.value, txbuf/' lib/Rcb4BaseLib/Rcb4BaseLib.py # 変数名のミスを修正

pip install lib

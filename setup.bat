@echo off
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if not exist lib mkdir lib
curl -o lib\RCB4Lib.zip https://kondo-robot.com/w/wp-content/uploads/RCB4Lib_for_Python_V100B.zip
tar -xf lib\RCB4Lib.zip -C lib && del lib\RCB4Lib.zip
xcopy /E /I /Y lib\RCB4Lib_for_Python_V100B\Rcb4Lib\Rcb4BaseLib.py lib\Rcb4BaseLib\ && rd /s /q lib\RCB4Lib_for_Python_V100B

black lib\Rcb4BaseLib\Rcb4BaseLib.py
powershell -Command "(Get-Content lib\Rcb4BaseLib\Rcb4BaseLib.py -Encoding UTF8) -replace 'return 0, Rcb4BaseLib.CmdOkType.Error.value, buf', 'return 0, Rcb4BaseLib.CmdOkType.Error.value, txbuf' | Set-Content lib\Rcb4BaseLib\Rcb4BaseLib.py -Encoding UTF8"

python -m pip install lib

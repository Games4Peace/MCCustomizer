@echo off

:ERROR_IN_LANG
set /p lang="Enter lang(he/ar): "
if not "%lang%"=="he" if not "%lang%"=="ar" goto ERROR_IN_LANG

:ERROR_IN_SERVER
set /p server="Enter server(1/2): "
if not "%server%"=="1" if not "%server%"=="2" goto ERROR_IN_SERVER

copy %lang%_s%server%_settings.json settings.json
copy %lang%_s%server%_servers.dat servers.dat

pyinstaller installer.py --name installer_%lang%_s%server% --onefile --add-data settings.json;data --add-data servers.dat;data

del settings.json servers.dat

pause
@echo off
setlocal

rem batファイルがあるディレクトリに移動
pushd "%~dp0"

py RunCSVCmp.py

popd

pause
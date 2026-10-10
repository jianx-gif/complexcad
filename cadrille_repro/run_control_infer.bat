@echo off
set ROOT=%~dp0..
if "%COMPLEXCAD_PY_CADREC%"=="" (set PY=%ROOT%\cadrec_env\Scripts\python.exe) else (set PY=%COMPLEXCAD_PY_CADREC%)
rem After the control training: inference for the control adapter, then the released checkpoint under the /100 input convention (baseline check)
cd /d %ROOT%\cadrille_repro
:wait
findstr /C:"done" %ROOT%\_review\cc_ctrl_lora\restarts.txt >nul 2>&1
if %errorlevel%==0 goto start
ping -n 301 127.0.0.1 >nul
goto wait
:start
ping -n 31 127.0.0.1 >nul
:loop
tasklist /FI "IMAGENAME eq python.exe" | find /I "python.exe" >nul
if %errorlevel%==0 (
  ping -n 61 127.0.0.1 >nul
  goto loop
)
%PY% -X utf8 run_cadrille.py --mode pc --batch 4 --adapter %ROOT%/_review/cc_ctrl_lora/final_adapter --outdir cadrille_ctrl --pc-scale100 --max-new-tokens 900 > %ROOT%\_review\cc_ctrl_infer.log 2>&1
%PY% -X utf8 run_cadrille.py --mode pc --batch 4 --outdir cadrille_scale100 --pc-scale100 --max-new-tokens 900 > %ROOT%\_review\cc_base100_infer.log 2>&1
echo done > %ROOT%\_review\cc_ctrl_lora\INFER_DONE

@echo off
rem Control run (same recipe on CAD-Recode-only data); waits until the ComplexCAD run AND its inference have finished
cd /d E:\3005\data\cadrille_repro
:wait
if exist E:\3005\data\_review\cc_full_lora\INFER_DONE goto start
ping -n 301 127.0.0.1 >nul
goto wait
:start
ping -n 61 127.0.0.1 >nul
set n=0
:loop
tasklist /FI "IMAGENAME eq python.exe" | find /I "python.exe" >nul
if %errorlevel%==0 (
  echo [%date% %time%] another python.exe is running, waiting 120 s >> E:\3005\data\_review\cc_ctrl_lora\restarts.txt
  ping -n 121 127.0.0.1 >nul
  goto loop
)
if not exist E:\3005\data\_review\cc_ctrl_lora mkdir E:\3005\data\_review\cc_ctrl_lora
E:\3005\data\cadrec_env\Scripts\python.exe -X utf8 train_closed_loop.py --rank 16 --epochs 3 --data E:/3005/data/_review/cc_ctrl --out E:/3005/data/_review/cc_ctrl_lora
findstr /C:"TRAINING DONE" E:\3005\data\_review\cc_ctrl_lora\stdout.txt >nul 2>&1
if %errorlevel%==0 goto done
set /a n+=1
echo [%date% %time%] training exited without DONE (restart %n%/6), waiting 90 s >> E:\3005\data\_review\cc_ctrl_lora\restarts.txt
if %n% GEQ 6 goto giveup
ping -n 91 127.0.0.1 >nul
goto loop
:giveup
echo [%date% %time%] giving up after 6 restarts >> E:\3005\data\_review\cc_ctrl_lora\restarts.txt
goto end
:done
echo [%date% %time%] done >> E:\3005\data\_review\cc_ctrl_lora\restarts.txt
:end

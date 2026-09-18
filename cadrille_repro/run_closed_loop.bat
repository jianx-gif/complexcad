@echo off
rem closed-loop training wrapper: resume from the last checkpoint after a crash; at most 6 restarts
cd /d E:\3005\data\cadrille_repro
set n=0
:loop
tasklist /FI "IMAGENAME eq python.exe" | find /I "python.exe" >nul
if %errorlevel%==0 (
  echo [%date% %time%] another python.exe is running, waiting 120 s >> E:\3005\data\_review\cc_full_lora\restarts.txt
  ping -n 121 127.0.0.1 >nul
  goto loop
)
E:\3005\data\cadrec_env\Scripts\python.exe -X utf8 train_closed_loop.py --rank 16 --epochs 3 --out E:/3005/data/_review/cc_full_lora
findstr /C:"TRAINING DONE" E:\3005\data\_review\cc_full_lora\stdout.txt >nul 2>&1
if %errorlevel%==0 goto done
set /a n+=1
echo [%date% %time%] training exited without DONE (restart %n%/6), waiting 90 s >> E:\3005\data\_review\cc_full_lora\restarts.txt
if %n% GEQ 6 goto giveup
ping -n 91 127.0.0.1 >nul
goto loop
:giveup
echo [%date% %time%] giving up after 6 restarts >> E:\3005\data\_review\cc_full_lora\restarts.txt
goto end
:done
echo [%date% %time%] done >> E:\3005\data\_review\cc_full_lora\restarts.txt
:end

@echo off
rem Third ComplexCAD run (C2): same data and recipe as the 10000-corpus run C, but with the random sample order
rem of the 8 September run (--sampler random) instead of the length-bucketed sampler, to test whether the
rem bucketed order causes the repetition loops. Waits for the main chain (ALL10K_DONE), then trains and infers.
setlocal EnableDelayedExpansion
set PY=E:\3005\data\cadrec_env\Scripts\python.exe
set R=E:\3005\data\_review
set LOG=%R%\run_c2.log
cd /d E:\3005\data\cadrille_repro
:wait
findstr /C:"ALL10K_DONE" %R%\run_all10k.log >nul 2>&1
if %errorlevel%==0 goto start
ping -n 121 127.0.0.1 >nul
goto wait
:start
echo [%date% %time%] c2 start >> %LOG%
if exist %R%\cc_full_lora_r2\INFER_DONE goto end
call :train %R%\cc_full_lora_r2 "--data E:/3005/data/_review/cc_full --out E:/3005/data/_review/cc_full_lora_r2 --rank 16 --epochs 3 --sampler random"
call :nopy
%PY% -X utf8 run_cadrille.py --mode pc --batch 4 --adapter E:/3005/data/_review/cc_full_lora_r2/final_adapter --outdir cadrille_cc_r2 --pc-scale100 --max-new-tokens 900 > %R%\cc_r2_infer.log 2>&1
echo done > %R%\cc_full_lora_r2\INFER_DONE
goto end

:train
set OUT=%~1
set ARGS=%~2
set n=0
:trainloop
call :nopy
if not exist "%OUT%" mkdir "%OUT%"
findstr /C:"TRAINING DONE" "%OUT%\stdout.txt" >nul 2>&1
if %errorlevel%==0 goto :eof
%PY% -X utf8 train_closed_loop.py %ARGS%
findstr /C:"TRAINING DONE" "%OUT%\stdout.txt" >nul 2>&1
if %errorlevel%==0 (
  echo [%date% %time%] %OUT% done >> %LOG%
  goto :eof
)
set /a n+=1
echo [%date% %time%] %OUT% exited without DONE (restart %n%/6), waiting 90 s >> %LOG%
if %n% GEQ 6 (
  echo [%date% %time%] %OUT% giving up >> %LOG%
  goto :eof
)
ping -n 91 127.0.0.1 >nul
goto trainloop

:nopy
tasklist /FI "IMAGENAME eq python.exe" | find /I "python.exe" >nul
if %errorlevel%==0 (
  ping -n 61 127.0.0.1 >nul
  goto nopy
)
goto :eof

:end
echo [%date% %time%] C2_DONE >> %LOG%
endlocal

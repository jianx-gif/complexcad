@echo off
rem Complete re-run of the four training arms on the 10000-model corpus (2026-09-13), strictly serial on the single GPU:
rem   C  ComplexCAD pc      : cc_full (6187 / 71)              -> cc_full_lora  -> predictions/cadrille_cc
rem   K  control            : cc_ctrl (6187 CAD-Recode / 71)  -> cc_ctrl_lora  -> predictions/cadrille_ctrl
rem   T  pc + text          : cc_full + description.txt        -> cc_text_lora  -> predictions/cadrille_cc_text
rem   D  pc + drawing       : cc_full + drawing.png (520 tok)  -> cc_draw_lora  -> predictions/cadrille_cc_draw
rem The assembly arm and the released-checkpoint baselines are not repeated: their data did not change.
setlocal EnableDelayedExpansion
set PY=E:\3005\data\cadrec_env\Scripts\python.exe
set R=E:\3005\data\_review
set LOG=%R%\run_all10k.log
cd /d E:\3005\data\cadrille_repro
echo [%date% %time%] all10k start >> %LOG%

rem ---------- C: ComplexCAD ----------
if not exist %R%\cc_full_lora\INFER_DONE (
  call :train %R%\cc_full_lora "--data E:/3005/data/_review/cc_full --out E:/3005/data/_review/cc_full_lora --rank 16 --epochs 3"
  call :nopy
  %PY% -X utf8 run_cadrille.py --mode pc --batch 4 --adapter E:/3005/data/_review/cc_full_lora/final_adapter --outdir cadrille_cc --pc-scale100 --max-new-tokens 900 > %R%\cc_full_infer.log 2>&1
  echo done > %R%\cc_full_lora\INFER_DONE
  echo [%date% %time%] C done >> %LOG%
)

rem ---------- K: control ----------
if not exist %R%\cc_ctrl_lora\INFER_DONE (
  call :train %R%\cc_ctrl_lora "--data E:/3005/data/_review/cc_ctrl --out E:/3005/data/_review/cc_ctrl_lora --rank 16 --epochs 3"
  call :nopy
  %PY% -X utf8 run_cadrille.py --mode pc --batch 4 --adapter E:/3005/data/_review/cc_ctrl_lora/final_adapter --outdir cadrille_ctrl --pc-scale100 --max-new-tokens 900 > %R%\cc_ctrl_infer.log 2>&1
  echo done > %R%\cc_ctrl_lora\INFER_DONE
  echo [%date% %time%] K done >> %LOG%
)

rem ---------- T: pc + text ----------
if not exist %R%\cc_text_lora\INFER_DONE (
  call :train %R%\cc_text_lora "--data E:/3005/data/_review/cc_full --out E:/3005/data/_review/cc_text_lora --rank 16 --epochs 3 --joint text"
  call :nopy
  %PY% -X utf8 run_cadrille.py --mode pc_text --batch 4 --adapter E:/3005/data/_review/cc_text_lora/final_adapter --outdir cadrille_cc_text --pc-scale100 --max-new-tokens 900 > %R%\cc_text_infer.log 2>&1
  echo done > %R%\cc_text_lora\INFER_DONE
  echo [%date% %time%] T done >> %LOG%
)

rem ---------- D: pc + drawing ----------
if not exist %R%\cc_draw_lora\INFER_DONE (
  call :train %R%\cc_draw_lora "--data E:/3005/data/_review/cc_full --out E:/3005/data/_review/cc_draw_lora --rank 16 --epochs 3 --joint drawing --draw-tokens 520"
  call :nopy
  %PY% -X utf8 run_cadrille.py --mode pc_draw --batch 2 --adapter E:/3005/data/_review/cc_draw_lora/final_adapter --outdir cadrille_cc_draw --pc-scale100 --draw-tokens 520 --max-new-tokens 900 > %R%\cc_draw_infer.log 2>&1
  echo done > %R%\cc_draw_lora\INFER_DONE
  echo [%date% %time%] D done >> %LOG%
)
goto end

rem ---------- subroutines ----------
:train
rem %1 = out dir, %2 = quoted training args; restart from checkpoint up to 6 times until TRAINING DONE
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
rem never start a GPU job while another python.exe is alive (serial GPU rule)
tasklist /FI "IMAGENAME eq python.exe" | find /I "python.exe" >nul
if %errorlevel%==0 (
  ping -n 61 127.0.0.1 >nul
  goto nopy
)
goto :eof

:end
echo [%date% %time%] ALL10K_DONE >> %LOG%
endlocal

@echo off
set ROOT=%~dp0..
if "%COMPLEXCAD_PY_CADREC%"=="" (set PY=%ROOT%\cadrec_env\Scripts\python.exe) else (set PY=%COMPLEXCAD_PY_CADREC%)
rem Three further closed-loop arms, strictly serial on the single GPU, after the control chain and its OCC evaluation:
rem   A  assembly loop   : fused assembly point cloud (512 pts) -> fastener placement program   (cc_asm_lora  -> predictions/cadrille_asm, baseline cadrille_asm_base)
rem   T  pc + text       : ComplexCAD point cloud + description.txt                              (cc_text_lora -> predictions/cadrille_cc_text)
rem   D  pc + drawing    : ComplexCAD point cloud + engineering drawing (520 visual tokens)      (cc_draw_lora -> predictions/cadrille_cc_draw)
setlocal EnableDelayedExpansion
set R=%ROOT%\_review
set LOG=%R%\run_arms.log
cd /d %ROOT%\cadrille_repro

:wait
findstr /C:"EVAL_CHAIN_DONE" %R%\eval_ctrl_chain.log >nul 2>&1
if %errorlevel%==0 goto start
ping -n 301 127.0.0.1 >nul
goto wait
:start
echo [%date% %time%] arms T+D restart (A done 12:49; T resumes from checkpoint) >> %LOG%

rem ---------- T: pc + text ----------
call :train %R%\cc_text_lora "--data %ROOT%/_review/cc_full --out %ROOT%/_review/cc_text_lora --rank 16 --epochs 3 --joint text"
call :nopy
%PY% -X utf8 run_cadrille.py --mode pc_text --batch 4 --adapter %ROOT%/_review/cc_text_lora/final_adapter --outdir cadrille_cc_text --pc-scale100 --max-new-tokens 900 > %R%\cc_text_infer.log 2>&1
echo [%date% %time%] T done >> %LOG%

rem ---------- D: pc + drawing (worst-case 3-step tests 09-09 11:15: A 512pts+<=1200ch 9.04 GB, T 9.04 GB, D 520 tok 10.33 GB; 1024 pts / 512pts+1500ch spilled to 14 GB) ----------
set DRAWTOK=520
goto dtrain
:dtrain
echo [%date% %time%] D smoke ok, draw-tokens !DRAWTOK! >> %LOG%
call :train %R%\cc_draw_lora "--data %ROOT%/_review/cc_full --out %ROOT%/_review/cc_draw_lora --rank 16 --epochs 3 --joint drawing --draw-tokens !DRAWTOK!"
call :nopy
%PY% -X utf8 run_cadrille.py --mode pc_draw --batch 2 --adapter %ROOT%/_review/cc_draw_lora/final_adapter --outdir cadrille_cc_draw --pc-scale100 --draw-tokens !DRAWTOK! --max-new-tokens 900 > %R%\cc_draw_infer.log 2>&1
echo [%date% %time%] D done >> %LOG%
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
echo [%date% %time%] ARMS_DONE >> %LOG%
endlocal

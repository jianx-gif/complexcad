@echo off
set ROOT=%~dp0..
if "%COMPLEXCAD_PY_CADREC%"=="" (set PY=%ROOT%\cadrec_env\Scripts\python.exe) else (set PY=%COMPLEXCAD_PY_CADREC%)
rem Self-healing launcher, run every 10 min by Task Scheduler (task cc_arms_watchdog):
rem  - if run_arms.log has ARMS_DONE: make sure eval_arms_chain.bat runs (until EVAL_ARMS_DONE), then nothing;
rem  - else if no run_arms_TD.bat wrapper is alive: (re)start it (idempotent: T/D resume from checkpoints, :nopy waits for GPU).
rem  (wmic is gone on this Windows build -> process checks via PowerShell; launches via WMI Create so the chain is not inside the task's job object)
set R=%ROOT%\_review
set WL=%R%\arms_watchdog.log
set PS=powershell.exe -NoProfile -NonInteractive -Command
findstr /C:"EVAL_ARMS_DONE" %R%\eval_arms_chain.log >nul 2>&1
if %errorlevel%==0 goto end
findstr /C:"ARMS_DONE" %R%\run_arms.log >nul 2>&1
if %errorlevel%==0 goto evalphase
%PS% "if (Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'cmd.exe' -and $_.CommandLine -like '*run_arms_TD*' }) { exit 0 } else { exit 1 }"
if %errorlevel%==0 goto end
echo [%date% %time%] no run_arms_TD wrapper alive - relaunching via WMI >> %WL%
%PS% "Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = 'cmd.exe /c %ROOT%\cadrille_repro\run_arms_TD.bat'; CurrentDirectory = '%ROOT%\cadrille_repro' } | Out-Null"
goto end
:evalphase
%PS% "if (Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'cmd.exe' -and $_.CommandLine -like '*eval_arms_chain*' }) { exit 0 } else { exit 1 }"
if %errorlevel%==0 goto end
echo [%date% %time%] arms done, eval chain not alive - launching via WMI >> %WL%
%PS% "Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = 'cmd.exe /c %ROOT%\_review\eval_arms_chain.bat'; CurrentDirectory = '%ROOT%\_review' } | Out-Null"
:end
exit /b 0

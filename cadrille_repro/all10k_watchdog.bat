@echo off
set ROOT=%~dp0..
if "%COMPLEXCAD_PY_CADREC%"=="" (set PY=%ROOT%\cadrec_env\Scripts\python.exe) else (set PY=%COMPLEXCAD_PY_CADREC%)
rem Self-healing launcher, run every 10 min by Task Scheduler (task cc_all10k_watchdog):
rem  - main chain run_all10k.bat until run_all10k.log has ALL10K_DONE;
rem  - then the third ComplexCAD run run_c2.bat until run_c2.log has C2_DONE;
rem  (idempotent: every arm resumes from its checkpoints, finished arms are skipped by INFER_DONE, :nopy waits for the GPU).
set R=%ROOT%\_review
set WL=%R%\all10k_watchdog.log
set PS=powershell.exe -NoProfile -NonInteractive -Command
findstr /C:"ALL10K_DONE" %R%\run_all10k.log >nul 2>&1
if %errorlevel%==0 goto c2phase
%PS% "if (Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'cmd.exe' -and $_.CommandLine -like '*run_all10k*' }) { exit 0 } else { exit 1 }"
if %errorlevel%==0 goto end
echo [%date% %time%] no run_all10k wrapper alive - relaunching via WMI >> %WL%
%PS% "Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = 'cmd.exe /c %ROOT%\cadrille_repro\run_all10k.bat'; CurrentDirectory = '%ROOT%\cadrille_repro' } | Out-Null"
goto end
:c2phase
findstr /C:"C2_DONE" %R%\run_c2.log >nul 2>&1
if %errorlevel%==0 goto end
%PS% "if (Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'cmd.exe' -and $_.CommandLine -like '*run_c2*' }) { exit 0 } else { exit 1 }"
if %errorlevel%==0 goto end
echo [%date% %time%] main chain done, no run_c2 wrapper alive - relaunching via WMI >> %WL%
%PS% "Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = 'cmd.exe /c %ROOT%\cadrille_repro\run_c2.bat'; CurrentDirectory = '%ROOT%\cadrille_repro' } | Out-Null"
:end
exit /b 0

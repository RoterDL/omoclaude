@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM do loop stop hook（Windows 版）：未完成则输出 JSON block，完成则清理状态文件

call :main
exit /b %ERRORLEVEL%

:main
if defined CLAUDE_PROJECT_DIR (
	set "project_dir=%CLAUDE_PROJECT_DIR%"
) else (
	set "project_dir=%CD%"
)
set "state_dir=%project_dir%\.claude"

set "stdin_tmp="
set "stdin_redirected=False"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "[Console]::IsInputRedirected"`) do set "stdin_redirected=%%A"
if /i "%stdin_redirected%"=="True" (
	set "temp_dir="
	for /f "usebackq delims=" %%T in (`powershell -NoProfile -Command "[System.IO.Path]::GetTempPath().Trim()"`) do set "temp_dir=%%T"
	if not defined temp_dir set "temp_dir=!state_dir!"
	if not "!temp_dir:~-1!"=="\" set "temp_dir=!temp_dir!\"
	set "stdin_tmp=!temp_dir!do_stop_hook_stdin_!RANDOM!!RANDOM!.txt"
	more > "!stdin_tmp!"
)

set "combined_reason="

if defined DO_TASK_ID (
	set "candidate=%state_dir%\do.%DO_TASK_ID%.local.md"
	if exist "!candidate!" (
		call :check_state_file "!candidate!" reason
		if defined reason set "combined_reason=!reason!"
	) else (
		goto cleanup_ok
	)
) else (
	if not exist "%state_dir%\do.*.local.md" goto cleanup_ok
	for %%F in ("%state_dir%\do.*.local.md") do (
		call :check_state_file "%%~fF" reason
		if defined reason (
			if defined combined_reason (
				set "combined_reason=!combined_reason! !reason!"
			) else (
				set "combined_reason=!reason!"
			)
		)
	)
)

if not defined combined_reason goto cleanup_ok

set "DO_BLOCK_REASON=%combined_reason%"
powershell -NoProfile -Command "$o=[ordered]@{decision='block';reason=$env:DO_BLOCK_REASON}; $o | ConvertTo-Json -Compress"
goto cleanup_ok

:cleanup_ok
if defined stdin_tmp del /f /q "%stdin_tmp%" >nul 2>nul
exit /b 0

REM ------------------------
REM 子程序：检查单个状态文件
REM 输出：若阻塞则设置 out_var 为原因字符串，否则为空
REM ------------------------
:check_state_file
setlocal EnableDelayedExpansion
set "state_file=%~1"
set "out_reason="

set "active_raw="
set "current_phase_raw="
set "max_phases_raw="
set "phase_name="
set "completion_promise="

set "line_no=0"
set "in_fm=0"

for /f "usebackq delims=" %%I in ("%state_file%") do (
	set "line=%%I"
	set /a line_no+=1
	if "!line_no!"=="1" (
		if "!line!"=="---" (
			set "in_fm=1"
		) else (
			goto fm_done
		)
	) else (
		if "!in_fm!"=="1" (
			if "!line!"=="---" goto fm_done
			for /f "tokens=1* delims=:" %%K in ("!line!") do (
				set "key=%%K"
				set "val=%%L"
				for /f "tokens=* delims= " %%V in ("!val!") do set "val=%%V"
				set "val=!val:"=!"

				if /i "!key!"=="active" set "active_raw=!val!"
				if /i "!key!"=="current_phase" set "current_phase_raw=!val!"
				if /i "!key!"=="max_phases" set "max_phases_raw=!val!"
				if /i "!key!"=="phase_name" set "phase_name=!val!"
				if /i "!key!"=="completion_promise" set "completion_promise=!val!"
			)
		)
	)
)

:fm_done
set "is_active=0"
if /i "!active_raw!"=="true" set "is_active=1"
if "!active_raw!"=="1" set "is_active=1"
if /i "!active_raw!"=="yes" set "is_active=1"
if /i "!active_raw!"=="on" set "is_active=1"
if "!is_active!"=="0" goto check_done

set "current_phase=1"
set "tmp=!current_phase_raw!"
if defined tmp (
	if /i "!tmp:~0,6!"=="phase_" (
		set "num=!tmp:~6!"
		set "non_digit="
		for /f "delims=0123456789" %%A in ("!num!") do set "non_digit=1"
		if not defined non_digit if defined num set "current_phase=!num!"
	)
)

set "max_phases=7"
set "tmp=!max_phases_raw!"
set "non_digit="
if defined tmp (
	for /f "delims=0123456789" %%A in ("!tmp!") do set "non_digit=1"
	if not defined non_digit set "max_phases=!tmp!"
)

if not defined phase_name (
	call :phase_name_for "!current_phase!" phase_name
)

if not defined completion_promise (
	set "completion_promise=<promise>DO_COMPLETE</promise>"
)

set "phases_done=0"
if !current_phase! GEQ !max_phases! set "phases_done=1"

set "promise_met=0"
if defined completion_promise (
	if defined stdin_tmp (
		findstr /L /C:"!completion_promise!" "%stdin_tmp%" >nul 2>nul && set "promise_met=1"
	)
	if "!promise_met!"=="0" (
		call :body_contains_promise "%state_file%" completion_promise body_found
		if "!body_found!"=="1" set "promise_met=1"
	)
)

if "!phases_done!"=="1" if "!promise_met!"=="1" (
	del /f /q "%state_file%" >nul 2>nul
	goto check_done
)

if "!phases_done!"=="0" (
	set "out_reason=do loop incomplete: current phase !current_phase!/!max_phases! (!phase_name!). Continue with remaining phases; update %state_file% current_phase/phase_name after each phase. Include completion_promise in final output when done: !completion_promise!. To exit early, set active to false."
) else (
	set "out_reason=do reached final phase (current_phase=!current_phase! / max_phases=!max_phases!, phase_name=!phase_name!), but completion_promise not detected: !completion_promise!. Please include this marker in your final output (or write it to %state_file% body), then finish; to force exit, set active to false."
)

:check_done
endlocal & set "%~2=%out_reason%" & exit /b 0

REM ------------------------
REM 子程序：根据 phase number 返回 phase_name（与 stop-hook.sh 一致）
REM ------------------------
:phase_name_for
setlocal
set "phase=%~1"
set "name=Phase %phase%"
if "%phase%"=="1" set "name=Discovery"
if "%phase%"=="2" set "name=Exploration"
if "%phase%"=="3" set "name=Clarification"
if "%phase%"=="4" set "name=Architecture"
if "%phase%"=="5" set "name=Implementation"
if "%phase%"=="6" set "name=Review"
if "%phase%"=="7" set "name=Summary"
endlocal & set "%~2=%name%"
exit /b 0

REM ------------------------
REM 子程序：检查 state_file 的 body（frontmatter 之后）是否包含 completion_promise
REM ------------------------
:body_contains_promise
setlocal EnableDelayedExpansion
set "state_file=%~1"
set "promise_var=%~2"
set "found=0"

call set "promise=%%%promise_var%%"
set "DO_BODY_FILE=%state_file%"
set "DO_BODY_PROMISE=%promise%"

powershell -NoProfile -Command "$file=$env:DO_BODY_FILE; $promise=$env:DO_BODY_PROMISE; $lines=Get-Content -LiteralPath $file; if(-not $lines -or $lines[0] -ne '---'){exit 1}; $end=-1; for($i=1;$i -lt $lines.Count;$i++){ if($lines[$i] -eq '---'){ $end=$i; break } }; if($end -lt 0){exit 1}; if(($end+1) -ge $lines.Count){ $body='' } else { $body=($lines[($end+1)..($lines.Count-1)] -join \"`n\") }; if($body -and $body.Contains($promise)){exit 0}else{exit 1}"
if not errorlevel 1 set "found=1"

endlocal & set "%~3=%found%" & exit /b 0

@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM 初始化 do 循环状态（Windows 版）

call :main %*
exit /b %ERRORLEVEL%

:main
set "max_phases=7"
set "completion_promise=<promise>DO_COMPLETE</promise>"
set "prompt="

:parse_args
if "%~1"=="" goto after_args

if /i "%~1"=="-h" goto show_help
if /i "%~1"=="--help" goto show_help

if /i "%~1"=="--max-phases" (
	if "%~2"=="" (
		call :die "--max-phases requires a value"
		exit /b 1
	)
	set "max_phases=%~2"
	shift
	shift
	goto parse_args
)

if /i "%~1"=="--completion-promise" (
	if "%~2"=="" (
		call :die "--completion-promise requires a value"
		exit /b 1
	)
	set "completion_promise=%~2"
	shift
	shift
	goto parse_args
)

if "%~1"=="--" (
	shift
	goto collect_prompt
)

set "arg=%~1"
if "!arg:~0,1!"=="-" (
	call :die "Unknown argument: %~1 (use --help)"
	exit /b 1
)
call :append_prompt "%~1"
shift
goto parse_args

:collect_prompt
if "%~1"=="" goto after_args
call :append_prompt "%~1"
shift
goto collect_prompt

:after_args
if not defined prompt (
	call :die "PROMPT is required (use --help)"
	exit /b 1
)

call :is_positive_int "%max_phases%" is_valid_int
if not "%is_valid_int%"=="1" (
	call :die "--max-phases must be a positive integer"
	exit /b 1
)

if defined CLAUDE_PROJECT_DIR (
	set "project_dir=%CLAUDE_PROJECT_DIR%"
) else (
set "project_dir=%CD%"
)
set "state_dir=%project_dir%\.claude"

if not exist "%state_dir%" mkdir "%state_dir%" >nul 2>nul

for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()"`) do set "epoch=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "$PID"`) do set "pid=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "[guid]::NewGuid().ToString('N').Substring(0,8)"`) do set "rand=%%A"

set "task_id=%epoch%-%pid%-%rand%"
set "state_file=%state_dir%\do.%task_id%.local.md"

set "phase_name=Discovery"

set "DO_MAX_PHASES=%max_phases%"
set "DO_COMPLETION_PROMISE=%completion_promise%"
set "DO_PHASE_NAME=%phase_name%"
set "DO_PROMPT=%prompt%"
set "DO_STATE_FILE=%state_file%"

powershell -NoProfile -Command "$sf=$env:DO_STATE_FILE; $max=[int]$env:DO_MAX_PHASES; $phase=$env:DO_PHASE_NAME; $promise=$env:DO_COMPLETION_PROMISE; $prompt=$env:DO_PROMPT; $nl=[Environment]::NewLine; $q=[char]34; $lines=@('---','active: true',('current_phase: ' + $q + 'phase_1' + $q),('phase_name: ' + $q + $phase + $q),('max_phases: ' + $max),('completion_promise: ' + $q + $promise + $q),'---','','# do loop state','','## Prompt',$prompt,'','## Notes','- Update frontmatter current_phase/phase_name as you progress','- When complete, include the frontmatter completion_promise in your final output'); $content=($lines -join $nl) + $nl; $enc=New-Object System.Text.UTF8Encoding $false; [System.IO.File]::WriteAllText($sf, $content, $enc);" >nul

if errorlevel 1 (
	call :die "Failed to write state file: %state_file%"
	exit /b 1
)

echo Initialized: %state_file%
echo task_id: %task_id%
echo phase: 1/%max_phases% (%phase_name%)
echo completion_promise: !completion_promise!
echo set DO_TASK_ID=!task_id!
exit /b 0

:show_help
call :usage
exit /b 0

:usage
echo Usage: setup-do.bat [options] PROMPT...
echo.
echo Creates project state file:
echo   .claude/do.{task_id}.local.md
echo.
echo Options:
echo   --max-phases N            Default: 7
echo   --completion-promise STR  Default: ^<promise^>DO_COMPLETE^</promise^>
echo   -h, --help                Show this help
exit /b 0

:die
echo ❌ %~1 >&2
exit /b 1

:append_prompt
set "part=%~1"
if defined prompt (
	set "prompt=%prompt% %part%"
) else (
	set "prompt=%part%"
)
exit /b 0

:is_positive_int
setlocal EnableDelayedExpansion
set "n=%~1"
set "ok=1"

if not defined n set "ok=0"
for /f "delims=0123456789" %%A in ("!n!") do set "ok=0"
if "!ok!"=="1" (
	if !n! LSS 1 set "ok=0"
)

endlocal & set "%~2=%ok%"
exit /b 0

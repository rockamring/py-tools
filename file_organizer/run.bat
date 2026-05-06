@echo off
chcp 65001 >nul
echo ==========================================
echo 游戏开发文档整理工具
echo ==========================================
echo.

if "%~1"=="" goto :help
if "%~1"=="preview" goto :preview
if "%~1"=="scan" goto :scan
if "%~1"=="execute" goto :execute
if "%~1"=="clean" goto :clean
goto :help

:preview
echo 运行预览模式...
python "%~dp0file_organizer.py" --preview
goto :end

:scan
echo 扫描文件统计...
python "%~dp0file_organizer.py" --scan-only
goto :end

:execute
echo 执行文件整理...
python "%~dp0file_organizer.py" --execute
goto :end

:clean
echo 执行整理并删除源文件...
echo 警告: 此操作将删除源文件！
set /p confirm=确认执行? (yes/no):
if /i "%confirm%"=="yes" (
    python "%~dp0file_organizer.py" --execute --delete-source
) else (
    echo 操作已取消
)
goto :end

:help
echo 用法: run.bat [命令]
echo.
echo 命令:
echo   preview  - 预览模式，不实际移动文件
echo   scan     - 仅扫描并显示统计
echo   execute  - 执行文件整理
echo   clean    - 执行整理并删除源文件（谨慎使用）
echo.
echo 示例:
echo   run.bat preview
echo   run.bat execute

:end
echo.
pause

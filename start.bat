@echo off
echo 🚀 啟動點子實驗室開發環境 (Hugo)...
echo.

echo 選擇啟動模式:
echo 1. Hugo 本地預覽 (推薦)
echo 2. 文章編輯器 + Hugo 預覽
echo 3. 僅文章編輯器
echo.
set /p choice=請選擇 (1-3): 

if "%choice%"=="1" goto hugo_only
if "%choice%"=="2" goto hugo_and_editor  
if "%choice%"=="3" goto editor_only
goto hugo_only

:hugo_only
echo 🏗️ 啟動 Hugo 本地預覽...
start cmd /k "hugo server -D --navigateToChanged --bind 0.0.0.0 --port 1313"
echo ⏳ 等待 Hugo 啟動...
timeout /t 3 /nobreak >nul
start http://localhost:1313
goto :end

:hugo_and_editor
echo 🏗️ 啟動 Hugo 預覽...
start cmd /k "hugo server -D --navigateToChanged --bind 0.0.0.0 --port 1313"
echo 🏗️ 啟動文章編輯器...
start "editor.html"
echo ⏳ 等待服務啟動...
timeout /t 3 /nobreak >nul
echo 📝 編輯器已開啟
echo 📱 Hugo 預覽: http://localhost:1313
goto :end

:editor_only
echo 🏗️ 啟動文章編輯器...
start "editor.html"
goto :end

:end
echo.
echo 💡 提示:
echo   - Hugo 預覽支援即時重載
echo   - 編輯器可下載 .md 檔案到 content/posts/
echo   - 使用 Ctrl+C 停止 Hugo 服務
pause 
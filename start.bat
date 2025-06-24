@echo off
echo 🚀 啟動點子實驗室開發環境...
echo.

REM 檢查容器是否已在運行
docker ps --filter "name=idea-hub-jekyll" --filter "status=running" | findstr "idea-hub-jekyll" >nul
if %errorlevel% == 0 (
    echo ✅ 容器已在運行
    echo 📱 網站地址: http://localhost:4000
    start http://localhost:4000
    goto :end
)

REM 檢查容器是否存在但已停止
docker ps -a --filter "name=idea-hub-jekyll" | findstr "idea-hub-jekyll" >nul
if %errorlevel% == 0 (
    echo 🔄 重新啟動現有容器...
    docker start idea-hub-jekyll
    echo ⏳ 等待服務啟動...
    timeout /t 5 /nobreak >nul
    start http://localhost:4000
    goto :end
)

REM 全新啟動
echo 🏗️ 首次啟動，正在建立容器...
docker-compose up -d
echo ⏳ 等待服務完全啟動 (約30秒)...
timeout /t 30 /nobreak >nul
start http://localhost:4000

:end
echo.
echo 💡 提示:
echo   - 容器會保持運行以加快下次啟動
echo   - 使用 'stop.bat' 停止容器
echo   - 使用 'logs.bat' 查看日誌
pause 
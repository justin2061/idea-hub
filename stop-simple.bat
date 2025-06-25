@echo off
echo ===========================================
echo      停止簡化版 Jekyll 預覽服務器
echo ===========================================
echo.

echo 停止容器...
docker-compose -f docker-compose-simple.yml down

echo.
echo ✅ Jekyll 預覽服務器已停止
echo.
pause 
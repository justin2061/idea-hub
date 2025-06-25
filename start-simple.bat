@echo off
echo ===========================================
echo      啟動簡化版 Jekyll 預覽服務器
echo ===========================================
echo.

echo 停止現有容器...
docker-compose down 2>nul

echo 啟動簡化版 Jekyll...
docker-compose -f docker-compose-simple.yml up -d

echo.
echo 等待服務器啟動...
timeout /t 10 /nobreak >nul

echo.
echo ===========================================
echo   🚀 Jekyll 預覽服務器已啟動！
echo   📱 本地預覽: http://localhost:4000
echo   🔄 LiveReload: http://localhost:35729
echo ===========================================
echo.

echo 顯示日誌 (Ctrl+C 停止)...
docker-compose -f docker-compose-simple.yml logs -f jekyll 
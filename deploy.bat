@echo off
echo 📦 準備部署到GitHub Pages...
echo.

echo 1️⃣ 檢查Git狀態...
git status

echo.
echo 2️⃣ 添加所有變更...
git add .

echo.
set /p message=請輸入commit訊息: 
if "%message%"=="" set message=更新網站內容

echo.
echo 3️⃣ 提交變更...
git commit -m "%message%"

echo.
echo 4️⃣ 推送到GitHub...
git push origin main

echo.
echo ✅ 部署完成！
echo 🌐 網站將在 2-3 分鐘後更新
echo 📱 GitHub Pages 網址: https://justin2061.github.io/idea-hub
echo.
echo 💡 提示: 首次部署需要在GitHub Repository設定中啟用Pages功能
pause 
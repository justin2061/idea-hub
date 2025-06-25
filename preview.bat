@echo off
echo 🎨 啟動 Jekyll 技術文章預覽...
echo.
echo 📌 主題：Minimal Mistakes (與 GitHub Pages 相同)
echo 📍 預覽網址：http://localhost:4000
echo 🔄 支援即時重載，修改檔案會自動更新
echo.
echo ⏳ 首次啟動需要下載主題，請耐心等待...
echo 📄 看到 "Server running..." 訊息後即可開啟瀏覽器
echo.
echo 🛑 按 Ctrl+C 停止伺服器
echo ==========================================
echo.

docker-compose -f docker-compose-preview.yml up --build 
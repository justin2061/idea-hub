# 🚀 CI/CD 部署完整指南

這份指南會帶你一步步設置完整的 CI/CD 自動化部署系統。

---

## 📋 前置需求

### 1. VM (虛擬機) 準備

你需要一台可以通過 SSH 訪問的 VM，可以是：
- ✅ AWS EC2
- ✅ Google Cloud Compute Engine
- ✅ DigitalOcean Droplet
- ✅ Azure Virtual Machine
- ✅ 任何支持 SSH 的 Linux 服務器

**最低配置：**
- OS: Ubuntu 20.04+ / Debian 11+
- RAM: 1GB+
- Storage: 10GB+
- 開放端口: 22 (SSH), 80 (HTTP), 443 (HTTPS)

### 2. 本地準備

- Git
- GitHub 帳號
- SSH 金鑰對

---

## 🔧 步驟 1：準備 VM

### 1.1 連接到你的 VM

```bash
ssh your-username@your-vm-ip
```

### 1.2 安裝必要軟體

```bash
# 更新系統
sudo apt update && sudo apt upgrade -y

# 安裝 Nginx (Web 服務器)
sudo apt install nginx -y

# 安裝 Ruby 和 Jekyll
sudo apt install ruby-full build-essential zlib1g-dev -y

# 配置 Ruby Gems
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 安裝 Jekyll 和 Bundler
gem install jekyll bundler

# 安裝 Git
sudo apt install git -y
```

### 1.3 設置部署目錄

```bash
# 創建部署目錄
sudo mkdir -p /var/www/idea-hub
sudo chown -R $USER:$USER /var/www/idea-hub
cd /var/www/idea-hub

# 創建目錄結構
mkdir -p current backups logs
```

### 1.4 配置 Nginx

```bash
# 創建網站配置
sudo nano /etc/nginx/sites-available/idea-hub
```

貼上以下內容：

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;  # 改成你的域名或 IP

    root /var/www/idea-hub/current;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # 緩存靜態資源
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip 壓縮
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # 安全性標頭
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    access_log /var/www/idea-hub/logs/access.log;
    error_log /var/www/idea-hub/logs/error.log;
}
```

啟用網站：

```bash
# 創建符號連結
sudo ln -s /etc/nginx/sites-available/idea-hub /etc/nginx/sites-enabled/

# 移除默認網站（可選）
sudo rm /etc/nginx/sites-enabled/default

# 測試配置
sudo nginx -t

# 重新載入 Nginx
sudo systemctl reload nginx

# 設置開機自動啟動
sudo systemctl enable nginx
```

### 1.5 設置防火牆

```bash
# 允許 SSH, HTTP, HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 啟用防火牆
sudo ufw enable

# 檢查狀態
sudo ufw status
```

---

## 🔑 步驟 2：設置 SSH 金鑰

### 2.1 在本地生成 SSH 金鑰

```bash
# 生成新的 SSH 金鑰對（如果還沒有）
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/idea-hub-deploy

# 這會生成兩個文件：
# ~/.ssh/idea-hub-deploy (私鑰) - 用於 GitHub Secrets
# ~/.ssh/idea-hub-deploy.pub (公鑰) - 添加到 VM
```

### 2.2 將公鑰添加到 VM

```bash
# 複製公鑰內容
cat ~/.ssh/idea-hub-deploy.pub

# SSH 到 VM
ssh your-username@your-vm-ip

# 添加公鑰到 authorized_keys
echo "你的公鑰內容" >> ~/.ssh/authorized_keys

# 設置正確的權限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### 2.3 測試 SSH 連接

```bash
# 在本地測試
ssh -i ~/.ssh/idea-hub-deploy your-username@your-vm-ip

# 如果成功連接，說明 SSH 金鑰設置正確
```

---

## 🔐 步驟 3：設置 GitHub Secrets

### 3.1 獲取私鑰內容

```bash
# 複製私鑰的完整內容（包括 BEGIN 和 END 行）
cat ~/.ssh/idea-hub-deploy
```

### 3.2 在 GitHub 添加 Secrets

1. 進入你的 GitHub Repository
2. 點擊 **Settings** > **Secrets and variables** > **Actions**
3. 點擊 **New repository secret**
4. 添加以下 secrets：

| Secret 名稱 | 值 | 說明 |
|------------|-----|------|
| `VM_HOST` | `123.456.789.0` | 你的 VM IP 或域名 |
| `VM_USER` | `ubuntu` | SSH 用戶名 |
| `VM_SSH_KEY` | `私鑰完整內容` | 從步驟 3.1 複製的私鑰 |
| `VM_DEPLOY_PATH` | `/var/www/idea-hub` | 部署目錄路徑 |

**可選 Secrets：**

| Secret 名稱 | 值 | 說明 |
|------------|-----|------|
| `SLACK_WEBHOOK` | `https://hooks.slack.com/...` | Slack 通知 webhook |
| `ANTHROPIC_API_KEY` | `sk-ant-api...` | 用於自動內容生成 |

---

## ✅ 步驟 4：測試部署

### 4.1 本地測試腳本

創建一個測試腳本來驗證 SSH 連接：

```bash
# 創建測試腳本
cat > test-deploy.sh << 'EOF'
#!/bin/bash
set -e

# 配置（根據你的實際情況修改）
VM_HOST="your-vm-ip"
VM_USER="your-username"
SSH_KEY="~/.ssh/idea-hub-deploy"
DEPLOY_PATH="/var/www/idea-hub"

echo "🧪 測試 SSH 連接..."
ssh -i "$SSH_KEY" "$VM_USER@$VM_HOST" "echo '✅ SSH 連接成功！'"

echo "📁 測試部署目錄..."
ssh -i "$SSH_KEY" "$VM_USER@$VM_HOST" "ls -la $DEPLOY_PATH"

echo "🚀 測試部署..."
ssh -i "$SSH_KEY" "$VM_USER@$VM_HOST" "echo 'Test deployment' > $DEPLOY_PATH/current/test.html"

echo "🌐 測試網站訪問..."
curl -I "http://$VM_HOST/test.html"

echo "✅ 所有測試通過！"
EOF

chmod +x test-deploy.sh
./test-deploy.sh
```

### 4.2 觸發 GitHub Actions

```bash
# 推送代碼到 main 分支
git add .
git commit -m "🚀 測試 CI/CD 部署"
git push origin main
```

### 4.3 查看部署狀態

1. 進入 GitHub Repository
2. 點擊 **Actions** 標籤
3. 查看最新的工作流運行狀態

---

## 📊 步驟 5：驗證部署

### 5.1 檢查網站

```bash
# 訪問你的網站
curl http://your-vm-ip

# 或在瀏覽器中打開
open http://your-vm-ip
```

### 5.2 查看日誌

```bash
# SSH 到 VM
ssh your-username@your-vm-ip

# 查看 Nginx 日誌
tail -f /var/www/idea-hub/logs/access.log
tail -f /var/www/idea-hub/logs/error.log

# 查看部署文件
ls -la /var/www/idea-hub/current/
```

---

## 🔧 步驟 6：進階設置

### 6.1 啟用 HTTPS（使用 Let's Encrypt）

```bash
# 安裝 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 獲取 SSL 證書
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自動續期
sudo certbot renew --dry-run
```

### 6.2 設置自動清理舊備份

```bash
# 創建清理腳本
cat > /var/www/idea-hub/cleanup-backups.sh << 'EOF'
#!/bin/bash
# 只保留最近 7 個備份
cd /var/www/idea-hub
ls -t backup-* | tail -n +8 | xargs -r rm -rf
EOF

chmod +x /var/www/idea-hub/cleanup-backups.sh

# 添加到 crontab（每天凌晨 3 點運行）
(crontab -l 2>/dev/null; echo "0 3 * * * /var/www/idea-hub/cleanup-backups.sh") | crontab -
```

### 6.3 設置監控和告警

創建健康檢查腳本：

```bash
cat > /var/www/idea-hub/health-check.sh << 'EOF'
#!/bin/bash

# 檢查 Nginx 狀態
if ! systemctl is-active --quiet nginx; then
    echo "❌ Nginx 未運行！嘗試重啟..."
    sudo systemctl start nginx
fi

# 檢查網站可訪問性
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost)
if [ "$HTTP_CODE" != "200" ]; then
    echo "❌ 網站返回 HTTP $HTTP_CODE"
    exit 1
fi

echo "✅ 健康檢查通過"
EOF

chmod +x /var/www/idea-hub/health-check.sh

# 每 5 分鐘檢查一次
(crontab -l 2>/dev/null; echo "*/5 * * * * /var/www/idea-hub/health-check.sh >> /var/www/idea-hub/logs/health.log 2>&1") | crontab -
```

---

## 🐛 故障排除

### 問題 1：SSH 連接失敗

**症狀：**
```
Permission denied (publickey)
```

**解決：**
```bash
# 檢查公鑰是否正確添加到 VM
cat ~/.ssh/authorized_keys

# 檢查權限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# 檢查 SSH 配置
sudo nano /etc/ssh/sshd_config
# 確保以下設置：
# PubkeyAuthentication yes
# PasswordAuthentication no

# 重啟 SSH
sudo systemctl restart sshd
```

### 問題 2：Nginx 404 錯誤

**症狀：**
訪問網站顯示 404 Not Found

**解決：**
```bash
# 檢查部署目錄
ls -la /var/www/idea-hub/current/

# 檢查 Nginx 配置
sudo nginx -t

# 檢查 Nginx 日誌
sudo tail -f /var/log/nginx/error.log

# 確保文件權限正確
sudo chown -R www-data:www-data /var/www/idea-hub/current/
sudo chmod -R 755 /var/www/idea-hub/current/
```

### 問題 3：GitHub Actions 部署失敗

**症狀：**
Actions 工作流在部署步驟失敗

**解決：**
```bash
# 檢查 GitHub Secrets 是否正確設置
# 檢查 VM 磁盤空間
df -h

# 檢查部署日誌
# 在 GitHub Actions 頁面查看詳細日誌
```

### 問題 4：Jekyll 構建失敗

**症狀：**
```
Liquid Exception: ... in ...
```

**解決：**
```bash
# 本地測試構建
bundle exec jekyll build --verbose

# 檢查 _config.yml
# 檢查文章的 front matter
# 檢查是否有語法錯誤
```

---

## 📈 性能優化

### 1. 啟用 HTTP/2

在 Nginx 配置中：
```nginx
listen 443 ssl http2;
```

### 2. 啟用瀏覽器緩存

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|ttf|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. 設置 CDN（可選）

使用 Cloudflare 或其他 CDN 服務來加速全球訪問。

---

## 📋 檢查清單

部署完成後，確認以下項目：

### 基礎設置
- [ ] VM 可以通過 SSH 訪問
- [ ] Nginx 正常運行
- [ ] 網站可以訪問（HTTP）
- [ ] GitHub Secrets 已正確設置

### 安全性
- [ ] SSH 只允許金鑰認證
- [ ] 防火牆已啟用
- [ ] HTTPS 已配置（推薦）
- [ ] 安全標頭已設置

### 自動化
- [ ] GitHub Actions 工作流正常運行
- [ ] 自動部署成功
- [ ] 自動測試通過
- [ ] 自動修復功能正常

### 監控
- [ ] 健康檢查腳本運行
- [ ] 日誌正常記錄
- [ ] 備份自動清理

---

## 🎉 下一步

恭喜！你已經成功設置了完整的 CI/CD 系統。

**現在你可以：**

1. **專注寫作**
   ```bash
   # 使用自動化工具生成文章
   cd _tools
   python article_generator.py -t comparison --title "我的文章"
   ```

2. **自動發布**
   ```bash
   git add .
   git commit -m "新增文章"
   git push
   # GitHub Actions 會自動構建、測試、部署！
   ```

3. **監控效果**
   - 查看 GitHub Actions 運行狀態
   - 查看網站訪問日誌
   - 收集讀者反饋

---

## 📞 獲取幫助

如果遇到問題：

1. 查看 GitHub Actions 日誌
2. 查看 VM 上的日誌文件
3. 查看 [Troubleshooting 章節](#-故障排除)
4. 提交 Issue 到 GitHub

---

**祝你部署順利！** 🚀

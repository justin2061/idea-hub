#!/bin/bash
# 一鍵生成並發布文章
# 使用方法：bash one_click_publish.sh [文章數量]

set -e  # 遇到錯誤立即退出

# 顏色定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 參數
ARTICLE_COUNT=${1:-1}  # 默認每個分類 1 篇
CATEGORIES=${2:-"all"}  # 默認所有分類

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🤖 自動內容生成與發布系統                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# 檢查是否在正確的目錄
if [ ! -f "_config.yml" ]; then
    echo -e "${YELLOW}⚠️  請在專案根目錄運行此腳本${NC}"
    exit 1
fi

# 檢查 API Key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  未設定 ANTHROPIC_API_KEY${NC}"
    echo "請執行: export ANTHROPIC_API_KEY='your-api-key'"
    echo "或在 .env 文件中設定"
    exit 1
fi

echo -e "${GREEN}📝 步驟 1/5: 檢查環境${NC}"
echo "  ✅ 專案目錄正確"
echo "  ✅ API Key 已設定"
echo ""

echo -e "${GREEN}🔍 步驟 2/5: 搜尋熱門話題並生成文章${NC}"
echo "  - 分類: $CATEGORIES"
echo "  - 每分類文章數: $ARTICLE_COUNT"
echo ""

cd _tools

# 安裝依賴（如果需要）
if ! python3 -c "import anthropic" 2>/dev/null; then
    echo "  📦 安裝依賴..."
    pip install -q anthropic requests pyyaml
fi

# 運行自動內容生成器
python3 auto_content_generator.py \
    --categories $CATEGORIES \
    --count $ARTICLE_COUNT

# 檢查是否成功生成文章
GENERATED_COUNT=$(ls -1 ../_posts/$(date +%Y-%m-%d)-*.md 2>/dev/null | wc -l)

if [ "$GENERATED_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}❌ 沒有生成任何文章${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ 成功生成 $GENERATED_COUNT 篇文章${NC}"
echo ""

cd ..

echo -e "${GREEN}📊 步驟 3/5: 生成文章列表${NC}"
echo "今天生成的文章："
ls -1 _posts/$(date +%Y-%m-%d)-*.md | while read file; do
    TITLE=$(grep "^title:" "$file" | sed 's/title: *"\(.*\)"/\1/')
    echo "  📄 $TITLE"
done
echo ""

echo -e "${GREEN}🔧 步驟 4/5: 運行測試${NC}"
# 簡單測試：檢查文章格式
for file in _posts/$(date +%Y-%m-%d)-*.md; do
    if [ -f "$file" ]; then
        # 檢查是否有 front matter
        if ! head -1 "$file" | grep -q "^---"; then
            echo -e "${YELLOW}  ⚠️  $file 缺少 front matter${NC}"
        else
            echo "  ✅ $(basename $file) 格式正確"
        fi
    fi
done
echo ""

echo -e "${GREEN}🚀 步驟 5/5: 發布到 GitHub${NC}"
read -p "是否要立即發布到 GitHub Pages？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Git 操作
    git add _posts/$(date +%Y-%m-%d)-*.md

    # 生成 commit 訊息
    COMMIT_MSG="🤖 自動生成 $GENERATED_COUNT 篇文章

分類：$CATEGORIES
生成時間：$(date '+%Y-%m-%d %H:%M:%S')

文章列表：
$(ls -1 _posts/$(date +%Y-%m-%d)-*.md | while read file; do
    TITLE=$(grep "^title:" "$file" | sed 's/title: *"\(.*\)"/\1/')
    echo "- $TITLE"
done)

由自動內容生成系統創建"

    git commit -m "$COMMIT_MSG"

    # 推送
    CURRENT_BRANCH=$(git branch --show-current)
    echo "  📤 推送到分支：$CURRENT_BRANCH"

    git push -u origin "$CURRENT_BRANCH"

    echo ""
    echo -e "${GREEN}✅ 發布完成！${NC}"
    echo ""
    echo "📊 部署狀態："
    echo "  - GitHub Actions 會自動構建和部署"
    echo "  - 查看進度：https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\).git/\1/')/actions"
    echo ""
    echo "🌐 你的文章將在幾分鐘後上線！"
else
    echo ""
    echo -e "${YELLOW}📝 跳過發布，文章已保存在 _posts/ 目錄${NC}"
    echo ""
    echo "手動發布步驟："
    echo "1. git add _posts/"
    echo "2. git commit -m '新增文章'"
    echo "3. git push"
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                  ✨ 完成！                              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"

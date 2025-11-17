#!/bin/bash
# 一鍵發布腳本
# 使用方法：bash quick_publish.sh path/to/article.md "commit message"

set -e  # 遇到錯誤立即退出

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 檢查參數
if [ $# -lt 1 ]; then
    echo -e "${RED}❌ 錯誤：缺少文件路徑${NC}"
    echo "使用方法：bash quick_publish.sh path/to/article.md \"commit message\""
    exit 1
fi

ARTICLE_FILE="$1"
COMMIT_MSG="${2:-新增文章}"

# 檢查文件是否存在
if [ ! -f "$ARTICLE_FILE" ]; then
    echo -e "${RED}❌ 錯誤：檔案不存在：$ARTICLE_FILE${NC}"
    exit 1
fi

# 獲取文件名
FILENAME=$(basename "$ARTICLE_FILE")
echo -e "${GREEN}📄 處理文章：$FILENAME${NC}"

# 檢查是否在 _drafts 目錄
if [[ "$ARTICLE_FILE" == *"_drafts"* ]]; then
    # 移動到 _posts 目錄
    DEST_DIR="$(dirname "$ARTICLE_FILE")/../_posts"
    mkdir -p "$DEST_DIR"

    echo -e "${YELLOW}📁 移動文章到 _posts 目錄...${NC}"
    cp "$ARTICLE_FILE" "$DEST_DIR/$FILENAME"
    ARTICLE_FILE="$DEST_DIR/$FILENAME"
    echo -e "${GREEN}✅ 已移動到：$ARTICLE_FILE${NC}"
fi

# 移除 _filled 後綴（如果有）
if [[ "$FILENAME" == *"_filled.md" ]]; then
    NEW_FILENAME="${FILENAME/_filled.md/.md}"
    NEW_PATH="$(dirname "$ARTICLE_FILE")/$NEW_FILENAME"

    echo -e "${YELLOW}📝 重新命名文件...${NC}"
    mv "$ARTICLE_FILE" "$NEW_PATH"
    ARTICLE_FILE="$NEW_PATH"
    FILENAME="$NEW_FILENAME"
    echo -e "${GREEN}✅ 新檔名：$FILENAME${NC}"
fi

# Git 操作
echo -e "${YELLOW}🔄 執行 Git 操作...${NC}"

# 回到專案根目錄
cd "$(dirname "$0")/.."

# 檢查文章中的 TODO
TODO_COUNT=$(grep -c "\[ \] TODO" "$ARTICLE_FILE" || true)
if [ "$TODO_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  警告：文章中還有 $TODO_COUNT 個 TODO 項目未完成${NC}"
    read -p "是否繼續發布？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}❌ 取消發布${NC}"
        exit 1
    fi
fi

# 檢查 Git 狀態
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ 錯誤：不在 Git 倉庫中${NC}"
    exit 1
fi

# 添加文件
git add "$ARTICLE_FILE"
echo -e "${GREEN}✅ 已添加文件到 Git${NC}"

# 提交
git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✅ 已提交：$COMMIT_MSG${NC}"

# 推送
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${YELLOW}🚀 推送到分支：$CURRENT_BRANCH${NC}"

git push -u origin "$CURRENT_BRANCH"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 發布成功！${NC}"
    echo ""
    echo -e "${GREEN}📊 發布摘要${NC}"
    echo "===================="
    echo "文章：$FILENAME"
    echo "分支：$CURRENT_BRANCH"
    echo "訊息：$COMMIT_MSG"
    echo "===================="
else
    echo -e "${RED}❌ 推送失敗，請檢查網路連接或權限${NC}"
    exit 1
fi

# 顯示文章資訊
echo ""
echo -e "${YELLOW}📄 文章資訊${NC}"
WORD_COUNT=$(wc -w < "$ARTICLE_FILE")
LINE_COUNT=$(wc -l < "$ARTICLE_FILE")
echo "字數：$WORD_COUNT"
echo "行數：$LINE_COUNT"

# 提取標題
TITLE=$(grep -m 1 "^title:" "$ARTICLE_FILE" | sed 's/title: *"\(.*\)"/\1/')
if [ -n "$TITLE" ]; then
    echo "標題：$TITLE"
fi

# 提取日期
DATE=$(grep -m 1 "^date:" "$ARTICLE_FILE" | sed 's/date: *//')
if [ -n "$DATE" ]; then
    echo "日期：$DATE"
fi

echo ""
echo -e "${GREEN}🎉 完成！你的文章已成功發布！${NC}"

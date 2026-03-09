
import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# === 配置区 ===
RSS_SOURCES = [
    "https://feeds.bbci.co.uk/news/rss.xml",           # 国际综合
    "https://www.theverge.com/rss/index.xml",         # 科技流行
    "https://36kr.com/feed",                          # 中国创业生态
    "https://www.jiqizhixin.com/rss",                 # ✅ 机器之心：AI论文、大模型、国产算力
    "https://www.leiphone.com/feed",                  # ✅ 雷峰网：AI落地、企业应用、投融资
    "https://rsshub.app/zhongguoai",                  # ✅ 中国AI聚合：知乎/微信/财新关键词
    "https://arstechnica.com/feed/",                  # ✅ Ars Technica：硬件、开源、安全深度
    "https://rsshub.app/github/trending/python",      # ✅ GitHub Python趋势：新工具发现
    "https://rsshub.app/arxiv/recent",                # ✅ arXiv最新论文：学术前沿
    "https://www.anandtech.com/rss"                   # ✅ AnandTech：芯片、GPU、CPU动态
]

EMAIL_FROM = "313413666@qq.com"
EMAIL_TO = "313413666@qq.com"  # 可设为多个，用逗号分隔
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SMTP_PASSWORD = "fljrdlvpovwwbhea"  # 请替换为应用专用密码

# === 主逻辑 ===
# 科技关键词库（中英文混合，覆盖主流技术热点）
TECH_KEYWORDS = {
    "AI", "大模型", "生成式AI", "量子", "芯片", "GPU", "自动驾驶",
    "机器人", "元宇宙", "Web3", "区块链", "RISC-V", "神经网络",
    "LLM", "Transformer", "AIGC", "算力", "开源", "开源模型",
    "大语言模型", "提示工程", "模型蒸馏", "MoE", "多模态", "推理加速"
}

def fetch_news():
    """
    从多个RSS源抓取新闻，仅保留包含科技关键词的内容
    返回结构化列表：[{'title', 'link', 'summary', 'source'}, ...]
    """
    articles = []
    
    for url in RSS_SOURCES:
        try:
            feed = feedparser.parse(url)
            # 若源解析失败，跳过
            if feed.bozo:
                continue
                
            for entry in feed.entries[:5]:  # 每源取前5条
                # 清洗标题与摘要，转为大写便于关键词匹配
                title = entry.title.strip().upper()
                summary = (entry.summary or "").strip().upper()
                
                # ✅ 关键过滤：仅保留含科技关键词的条目
                if any(kw in title or kw in summary for kw in TECH_KEYWORDS):
                    # 截断摘要，避免过长
                    summary_clean = entry.summary[:150] + "..." if len(entry.summary or "") > 150 else (entry.summary or "")
                    
                    articles
def send_email(articles):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = f"每日新闻简报 · {datetime.now().strftime('%Y-%m-%d')}"

    body = "<h2>📅 每日新闻简报</h2><hr>"
    for article in articles:
        body += f"""
        <h3>{article['title']}</h3>
        <p><strong>来源：</strong>{article['source']}</p>
        <p>{article['summary']}</p>
        <p><a href="{article['link']}">阅读全文 →</a></p>
        <hr>
        """
    
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_FROM, SMTP_PASSWORD)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()

if __name__ == "__main__":
    print("正在抓取新闻...")
    news = fetch_news()
    print(f"共获取 {len(news)} 条新闻")
    send_email(news)
    print("邮件已发送！")

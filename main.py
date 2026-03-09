
import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# === 配置区 ===
RSS_SOURCES = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.theverge.com/rss/index.xml",
    "https://36kr.com/feed"
]

EMAIL_FROM = "313413666@qq.com"
EMAIL_TO = "313413666@qq.com"  # 可设为多个，用逗号分隔
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SMTP_PASSWORD = "fljrdlvpovwwbhea"  # 请替换为应用专用密码

# === 主逻辑 ===
def fetch_news():
    articles = []
    for url in RSS_SOURCES:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # 每源取前5条
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.summary[:150] + "..." if len(entry.summary) > 150 else entry.summary,
                'source': feed.feed.title
            })
    return articles

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

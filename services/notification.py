"""
通知服务 - 邮件 + Server酱微信推送
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import requests


def send_email_alert(to_email: str, subject: str, body: str):
    """
    发送邮件通知
    
    需要在 .env 中配置:
    - SMTP_HOST: SMTP 服务器地址
    - SMTP_PORT: SMTP 端口 (默认 587)
    - SMTP_USER: 发件人邮箱
    - SMTP_PASSWORD: 邮箱密码
    - SMTP_FROM: 发件人显示名称
    """
    smtp_host = os.environ.get('SMTP_HOST')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    smtp_from = os.environ.get('SMTP_FROM', '旷了吗')

    if not all([smtp_host, smtp_user, smtp_password]):
        print(f"[通知跳过] 邮件配置不完整，无法发送邮件到 {to_email}")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = f"{smtp_from} <{smtp_user}>"
        msg['To'] = to_email
        msg['Subject'] = subject

        # 邮件正文（支持HTML）
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
                <h2 style="margin: 0;">🚨 {subject}</h2>
            </div>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 0 0 10px 10px;">
                <p style="font-size: 16px; line-height: 1.6;">{body}</p>
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
                <p style="color: #888; font-size: 12px;">
                    此邮件由「旷了吗」系统自动发送<br>
                    发送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html, 'html', 'utf-8'))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [to_email], msg.as_string())

        print(f"[通知] 邮件已发送至 {to_email}: {subject}")
        return True
    except Exception as e:
        print(f"[通知失败] 邮件发送失败: {e}")
        return False


def send_wechat_alert(sckey: str, title: str, content: str):
    """
    通过 Server酱 发送微信通知
    
    注册地址: https://sct.ftqq.com/
    获取 SCKEY 后在 .env 中配置 SERVERCHAN_SCKEY
    
    Server酱免费版支持 Markdown，但不支持加粗等格式
    """
    if not sckey:
        print("[通知跳过] 未配置 Server酱 SCKEY")
        return False

    try:
        url = f"https://sctapi.ftqq.com/{sckey}.send"
        data = {
            "title": f"🚨 {title}",
            "desp": content
        }
        resp = requests.post(url, data=data, timeout=10)
        result = resp.json()
        if result.get('code') == 0 or result.get('errno') == 0:
            print(f"[通知] Server酱推送成功: {title}")
            return True
        else:
            print(f"[通知失败] Server酱: {result}")
            return False
    except Exception as e:
        print(f"[通知失败] Server酱异常: {e}")
        return False


def notify_guardian_missed(
    guardian_email: str,
    guardian_sckey: str,
    student_name: str,
    course_name: str,
    start_time: str,
    location: str
):
    """
    通知监护人：学生旷课未签到
    
    同时发送邮件和微信（如果都配置了）
    """
    subject = f"⚠️ {student_name} 还没到课"
    body = f"""
    <p>家长您好，<strong>{student_name}</strong> 今天的 <strong>{course_name}</strong> 课程</p>
    <p>已于 <strong>{start_time}</strong> 开始</p>
    <p>截至目前，系统未检测到签到记录。</p>
    <p style="color: #e74c3c; font-size: 18px; font-weight: bold; margin: 20px 0;">
        请您确认孩子是否安全到达教室。
    </p>
    {"<p>📍 教室位置：" + location + "</p>" if location else ""}
    <p>本通知由「旷了吗」自动发送。如有疑问，请联系孩子确认情况。</p>
    """
    content_md = f"""**{student_name}** 还没到课

课程：{course_name}
时间：{start_time}
{"地点：" + location if location else ""}

请确认孩子是否安全到达教室。"""

    # 发送邮件
    if guardian_email:
        send_email_alert(guardian_email, subject, body)

    # 发送微信
    if guardian_sckey:
        send_wechat_alert(guardian_sckey, subject, content_md)


def notify_guardian_checkin(
    guardian_email: str,
    guardian_sckey: str,
    student_name: str,
    course_name: str,
    checkin_time: str
):
    """通知监护人：学生已签到（可选，给家长安心）"""
    subject = f"✅ {student_name} 已到课"
    body = f"""
    <p>家长您好，<strong>{student_name}</strong> 已完成 <strong>{course_name}</strong> 的签到。</p>
    <p>签到时间：{checkin_time}</p>
    <p style="color: #27ae60; font-size: 14px;">
        孩子平安到课，请放心 😊
    </p>
    """
    content_md = f"""✅ {student_name} 已到课

课程：{course_name}
签到时间：{checkin_time}

孩子平安到课，请放心。"""

    if guardian_email:
        send_email_alert(guardian_email, subject, body)
    if guardian_sckey:
        send_wechat_alert(guardian_sckey, subject, content_md)

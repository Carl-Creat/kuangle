# 旷了吗 - 学生安全签到工具

> "今天我上课了吗？让家长放心！"

一个专为学生打造的自愿式安全签到工具，帮助家长了解孩子的到课情况，减少"孩子到底有没有去上课"的焦虑。

## 核心功能

- 📅 **课程表管理** - 学生自主添加每周课程，系统自动推送到课提醒
- ✅ **一键签到** - 上课前收到提醒，点击即可报平安
- 🚨 **超时预警** - 超过课程开始时间未签到，自动通知家长
- 👨‍👩‍👧 **家长监护** - 一个学生可绑定多位监护人，实时查看签到记录
- 📊 **签到报表** - 周报/月报统计，让家长了解孩子的出勤情况

## 目标用户

- 住校大学生 / 高中生（远离家长独立生活）
- 家长期望了解孩子出勤情况
- 学生自愿使用，无强制管控

## 技术栈

- 后端：Python 3.11 + Flask
- 数据库：SQLite（本地）/ PostgreSQL（生产）
- 前端：HTML5 + Tailwind CSS（移动端优先）
- 通知：Email（SMTP）+ 微信推送（企业微信/Server酱）

## 项目结构

```
旷了吗/
├── app.py                  # Flask 主应用
├── models.py               # 数据库模型
├── routes/
│   ├── auth.py             # 注册/登录
│   ├── schedule.py         # 课程表管理
│   ├── checkin.py          # 签到逻辑
│   └── guardian.py         # 监护人管理
├── services/
│   ├── notification.py     # 通知服务
│   └── scheduler.py        # 定时任务（检查超时）
├── templates/              # HTML 模板
├── static/                 # CSS/JS/图片
├── requirements.txt
└── README.md
```

## 运行

```bash
pip install -r requirements.txt
python app.py
# 访问 http://localhost:5000
```

## License

MIT

# 📚 旷了吗 - 学生安全签到工具

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

**让学生安全，让家长安心**

一个专为学生打造的自愿式安全签到工具。设定课程表 → 每天签到报平安 → 超时自动通知家长

📖 [快速开始](#快速开始) · 📖 [部署指南](DEPLOY.md) · 🐛 [报告问题](https://github.com/Carl-Creat/kuangle/issues)

</div>

---

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| 📅 **课程表管理** | 自主添加每周课程，自动推送上课提醒 |
| ✅ **一键签到** | 收到提醒后点击即可报平安 |
| 🚨 **超时预警** | 超时未签到，家长自动收到邮件/微信通知 |
| 👨‍👩‍👧 **家长监护** | 绑定监护人，实时查看孩子的出勤记录 |
| 📊 **签到报表** | 周报统计，出勤情况一目了然 |

---

## ⚡ 快速开始

### 🖱️ Windows 用户（下载即用，最简单）

> **像下载 App 一样，无需安装 Python，双击就能用！**

**Step 1.** 下载便携版（最新版本）：👇
> 前往 [Releases 页面](https://github.com/Carl-Creat/kuangle/releases) 下载 `kuangle-windows-portable.zip`

**Step 2.** 解压到任意文件夹

**Step 3.** **双击 `启动旷了吗.exe`** → 浏览器自动打开 http://localhost:5000

> 💡 首次使用建议先运行 `一键安装旷了吗.bat` 安装依赖

---

### 🍎 macOS / Linux / 程序员用户

```bash
# 克隆项目
git clone https://github.com/Carl-Creat/kuangle.git
cd kuangle

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 启动
python app.py
```

访问 http://localhost:5000

---

### 🐳 Docker 部署

```bash
docker-compose up -d
```

访问 http://localhost:5000

---

## 👨‍👩‍👧 使用流程

```
学生端                          家长端
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 注册（选"学生"角色）      1. 注册（选"家长"角色）
         ↓                               ↓
2. 添加课程表                  2. 等待孩子绑定
         ↓
3. 每天上课前收到提醒
         ↓
4. 点击"立即签到"  ──────────→  实时收到孩子到课通知 ✅
         ↓
   超时未签到  ──────────────→  家长收到超时预警 🚨
```

---

## 📱 功能预览

### 学生端
- 📅 今日课程一览 + 签到状态
- ✅ 一键签到（点击即完成）
- ⏰ 超时提醒（没签到会变红）
- 📊 本周出勤率环形图
- 👨‍👩‍👧 绑定监护人

### 家长端
- 👀 查看已绑定的孩子的今日到课情况
- 🚨 未签到实时预警
- ⚙️ 通知渠道配置（邮件/微信）

---

## 🔧 高级配置

### 微信通知（Server酱，免费）

1. 打开 https://sct.ftqq.com → 用 GitHub 登录
2. 复制你的 **SCKEY**
3. 在运行目录新建 `.env` 文件：
```env
SERVERCHAN_SCKEY=你的SCKEY
```
4. 重启程序即可收到微信推送

### 邮件通知

```env
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
SMTP_USER=your@qq.com
SMTP_PASSWORD=your_auth_code
SMTP_FROM=旷了吗
```

### ☁️ 让程序 24 小时在线

使用方式一（便携版） + 内网穿透工具（如 [Sakura Frp](https://www.natfrp.com/)）即可将 localhost:5000 暴露到公网。

---

## 🏗️ 项目结构

```
kuangle/
├── app.py                     # Flask 主应用
├── models.py                  # 数据库模型（已在 app.py 中）
├── services/
│   ├── notification.py        # 邮件 + 微信通知服务
│   └── scheduler.py          # 定时任务（检查旷课）
├── templates/
│   ├── index.html             # 首页（产品介绍）
│   ├── register.html          # 注册（选学生/家长角色）
│   ├── login.html             # 登录
│   ├── student_dashboard.html # 学生控制台
│   └── guardian_dashboard.html # 家长控制台
├── tools/
│   └── installer.iss         # Inno Setup 安装向导脚本
├── requirements.txt
├── DEPLOY.md                  # 详细部署指南
├── README.md
├── 一键安装旷了吗.bat          # Windows 一键安装脚本
├── 启动旷了吗.bat              # Windows 启动脚本
└── kuangle.spec               # PyInstaller 打包配置
```

---

## 🐛 常见问题

| 问题 | 解决方法 |
|------|---------|
| 启动后浏览器打不开 | 换个端口：`python app.py --port 8080` |
| 微信通知没收到 | 检查 SCKEY 是否正确，Server酱是否开启推送 |
| 数据存储在哪 | `data/kuangle.db`，换电脑前备份此文件 |
| 如何让程序后台运行 | Windows 使用 `pythonw app.py` 或用 Docker |
| 想卸载 | 便携版直接删除文件夹，无残留 |

详细说明见 [DEPLOY.md](DEPLOY.md)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 License

MIT License

---

<div align="center">

**愿每位学子平安到课** 📚

*如果你觉得这个项目有用，请点个 ⭐ 支持一下！*

</div>

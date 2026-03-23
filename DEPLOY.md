# 🎓 旷了吗 - 部署指南

本指南面向不同技术水平的用户，选择最适合你的方式。

---

## 方式一：🖱️ 下载即用（推荐 · 普通用户）

> **像下载 App 一样简单，双击就能用**

### 第一步：下载

点击 GitHub Releases 页面，下载最新版本的压缩包：
👉 https://github.com/Carl-Creat/kuangle/releases

你会看到类似这样的文件：
```
kuangle-v1.0-windows-portable.zip   ← 下载这个
```

### 第二步：解压

右键压缩包 →「全部解压缩」→ 打开 `kuangle-windows` 文件夹，你会看到：

```
kuangle-windows/
├── 📄 启动旷了吗.exe      ← 双击这个！
├── 📄 一键安装.bat
├── 📄 app.py
├── 📄 data/               ← 你的数据在这里
├── 📄 templates/
└── 📄 requirements.txt
```

### 第三步：运行

**双击 `启动旷了吗.exe`**

浏览器会自动打开 http://localhost:5000

🎉 现在去注册账号开始使用吧！

### 第四步（可选）：配置微信通知

如果想启用微信提醒，在解压后的文件夹里新建一个文件 `.env`：

```env
# Server酱 - 微信通知（免费）
# 申请地址：https://sct.ftqq.com （用 GitHub 账号登录）
SERVERCHAN_SCKEY=你的SCKEY

# 邮件通知（可选）
SMTP_HOST=smtp.qq.com
SMTP_USER=your_email@qq.com
SMTP_PASSWORD=your_auth_code
```

配置好后重启程序即可。

---

## 方式二：📦 打包版安装程序（.exe 安装向导）

> 跟安装 QQ、微信一样，有个安装向导引导你完成

下载 `kuangle-setup.exe`（待发布），双击运行：

```
欢迎使用 旷了吗 安装向导
━━━━━━━━━━━━━━━━━━━━━━━━━━
下一步 → 选择安装位置 → 完成安装
                                  
安装完成后，桌面会有快捷方式，
开始菜单里有程序列表
```

> 如需生成此安装程序，可参考下方「如何生成安装程序」章节。

---

## 方式三：💻 命令行部署（面向开发者）

### 环境要求

- Python 3.9 或更高
- 网络连接（用于安装依赖）

### 快速安装

```bash
# 1. 克隆或下载本项目
git clone https://github.com/Carl-Creat/kuangle.git
cd kuangle

# 2. 安装依赖（推荐使用国内镜像）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 启动
python app.py
```

访问 http://localhost:5000

### 使用 Docker 部署（推荐生产环境）

```bash
# 1. 构建镜像
docker build -t kuangle .

# 2. 运行容器
docker run -d -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -e SMTP_HOST=smtp.qq.com \
  -e SMTP_USER=your@qq.com \
  -e SMTP_PASSWORD=your_auth_code \
  --name kuangle \
  kuangle
```

### 使用 Docker Compose 部署（推荐）

```bash
# 1. 创建 docker-compose.yml（已在仓库中）
# 2. 复制 .env.example 为 .env 并填写配置
cp .env.example .env

# 3. 启动
docker-compose up -d
```

---

## 方式四：☁️ 云端部署（让程序 24 小时在线）

### Railway（免费额度够用）

1. 访问 https://railway.app
2. 用 GitHub 登录
3. New Project → Deploy from GitHub → 选择 `kuangle` 仓库
4. Railway 会自动检测 Python 项目并部署
5. 在 Variables 中添加环境变量（SMTP 配置等）

### Render（免费额度）

1. 访问 https://render.com
2. 用 GitHub 登录
3. New → Web Service
4. Connect 你的 kuangle 仓库
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn app:app`（需要先 `pip install gunicorn`）

### 阿里云/腾讯云轻量应用服务器

```bash
# 在服务器上
yum install -y docker.io   # CentOS
apt install -y docker.io   # Ubuntu

systemctl start docker
docker pull python:3.11-slim

cd /path/to/kuangle
docker build -t kuangle .
docker run -d -p 5000:5000 -v ./data:/app/data --name kuangle kuangle
```

---

## 如何生成安装程序（打包为 .exe）

### 生成便携版压缩包（最简单）

```bash
# 1. 安装打包工具
pip install pyinstaller

# 2. 打包
pyinstaller kuangle.spec

# 3. 找到输出文件
# dist/kuangle/ 目录下就是可分发的程序
# 压缩整个文件夹分享给别人即可
```

### 生成 Windows 安装向导（推荐）

使用 [Inno Setup](https://jrsoftware.org/isdl.php)（免费）：

1. 下载并安装 Inno Setup
2. 打开 `installer.iss` 文件（仓库中已提供）
3. 点击 Build → Compile
4. 生成的 `kuangle-setup.exe` 就是安装程序

> 📌 `installer.iss` 文件已包含在本仓库的 `tools/` 目录下。

---

## 常见问题

### Q: 启动后浏览器打不开？
确保没有其他程序占用了 5000 端口，可改为：
```bash
python app.py --port 8080
```
然后访问 http://localhost:8080

### Q: 数据库在哪里？换电脑数据会丢吗？
数据库文件在 `data/kuangle.db`
换电脑前把这个文件备份，换到新电脑后放到新目录的 data 文件夹即可。

### Q: 微信通知怎么配置？
1. 打开 https://sct.ftqq.com
2. 用 GitHub 账号登录
3. 复制你的 SCKEY
4. 在 `.env` 文件中添加 `SERVERCHAN_SCKEY=你的SCKEY`
5. 重启程序即可

### Q: 想让程序 24 小时在线？
使用方式一（便携版）或方式三（Docker），然后配置内网穿透：
```bash
# 安装 frp 或使用 Sakura Frp
# 将 localhost:5000 暴露到公网
```

### Q: 如何卸载？
- **便携版**：直接删除文件夹即可，无残留
- **安装版**：通过「控制面板 → 程序和功能」卸载
- **Docker**：`docker stop kuangle && docker rm kuangle`

---

## 数据备份与迁移

数据库位置：`data/kuangle.db`

```bash
# 备份
copy data\kuangle.db backups\kuangle_backup_2026-03-23.db

# 迁移（复制到新电脑的 data 目录即可）
```

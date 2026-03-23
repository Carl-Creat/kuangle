# -*- coding: utf-8 -*-
"""
PyInstaller 打包配置 - 旷了吗
将 Flask 应用打包为独立的 Windows 可执行文件

使用方法:
    pip install pyinstaller
    pyinstaller kuangle.spec
    # 打包完成后，dist/kuangle.exe 即为可执行文件
"""

import os
import sys
import shutil

block_cipher = None

# 项目根目录
ROOT = os.path.dirname(os.path.abspath(SPEC))

# 需要包含的数据文件
datas = [
    # 模板
    (os.path.join(ROOT, 'templates'), 'templates'),
    # 静态文件（未来可扩展）
    # (os.path.join(ROOT, 'static'), 'static'),
]

# 运行时生成的数据目录（用户数据放这里）
# 打包后 data/ 目录会被创建在 exe 同级目录
data_folder = os.path.join(ROOT, 'data')

# 如果 data 目录存在就包含它
if os.path.exists(data_folder):
    datas.append((data_folder, 'data'))

a = Analysis(
    [os.path.join(ROOT, 'app.py')],          # 主入口
    pathex=[ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'werkzeug',
        'apscheduler',
        'sqlalchemy',
        'email.mime',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',      # 不需要数值计算，排除减小体积
        'pandas',
        'scipy',
        'PIL',        # 如果不用图片处理
        'cv2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='kuangle',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,          # 显示控制台窗口（方便看日志/调试）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,             # 可指定图标: icon='kuangle.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='kuangle',
)

# 打包完成后，自动创建 data 目录（用于存放数据库）
# 并复制 README 和 使用说明
"""
EOF - 打包后请手动操作:
1. 在 dist/kuangle 目录下创建 data 文件夹
2. dist/kuangle/data/ 即为应用数据目录
3. 数据库文件将保存在这里，重启后数据不丢失
4. 通知功能的 SMTP 配置，需要在 dist/kuangle/ 下创建 .env 文件
"""

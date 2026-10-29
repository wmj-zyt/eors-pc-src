# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# 定义一个函数来递归收集目录下所有文件，保持原有的目录结构
def collect_all_files(source_dir, target_dir):
    """递归收集目录下所有文件"""
    datas = []
    if not os.path.exists(source_dir):
        print(f"警告: 目录不存在 - {source_dir}")
        return datas
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_path = os.path.join(root, file)
            # 计算相对路径
            rel_path = os.path.relpath(root, source_dir)
            if rel_path == '.':
                target_path = target_dir
            else:
                target_path = os.path.join(target_dir, rel_path)
            datas.append((source_path, target_path))
    return datas

# 收集所有模块目录（保持原有目录结构）
all_datas = []

# 1. 收集P08_Activity（主程序入口和界面逻辑）
all_datas.extend(collect_all_files('P08_Activity', 'P08_Activity'))

# 2. 收集P03_Components（自定义组件）
all_datas.extend(collect_all_files('P03_Components', 'P03_Components'))

# 3. 收集P04_Model（AI模型）
all_datas.extend(collect_all_files('P04_Model', 'P04_Model'))

# 4. 收集P06_Utils（工具类）
all_datas.extend(collect_all_files('P06_Utils', 'P06_Utils'))

# 5. 收集P07_View（UI文件和生成的Python文件）
all_datas.extend(collect_all_files('P07_View', 'P07_View'))

# 6. 收集P02_Resource（资源文件：配置、图片等）
all_datas.extend(collect_all_files('P02_Resource', 'P02_Resource'))

# 7. 收集P05_Database（数据库文件，如果存在）
if os.path.exists('P05_Database'):
    all_datas.extend(collect_all_files('P05_Database', 'P05_Database'))

# 基础数据文件（图标和启动画面）
base_datas = [
    ('logo.ico', '.'), 
    ('EORS.png', '.')
]
all_datas.extend(base_datas)

# 分析配置
a = Analysis(
    ['main.py'],  # 主入口文件在根目录
    pathex=[],  # 添加所有模块路径
    binaries=[],
    datas=all_datas,
    hiddenimports=[
        'scipy.special._cdflib',
        # 添加可能的隐藏导入
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# 启动画面配置
# ⚠️ 注释掉 Splash 相关代码
splash = Splash('EORS.png',
                 binaries=a.binaries,
                 datas=a.datas,
                 text_pos=(10, 397),
                 text_size=10,
                 text_color='#2b2b2b',
                 minify_script=True)

pyz = PYZ(a.pure)

# 打包成单个exe文件
exe = EXE(
    pyz,
    a.scripts,
    splash,
    splash.binaries,
    a.binaries,
    a.datas,
    [],
    name='EORS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 如果安装了UPX可以改为True
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
)
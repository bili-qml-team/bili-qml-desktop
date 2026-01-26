<h1 align="center">B站问号榜 (Bilibili Question-Mark Leaderboard)</h1>

<p align="center">
  <strong>分享抽象的视频，自动同步弹幕，打造Bilibili的抽象视频排行榜。</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/pyqt6-6.4.2+-green" alt="Qt Framework">
  <img src="https://img.shields.io/badge/license-GPL--3.0-orange" alt="License">
</p>

---

## 📖 项目简介

B站问号榜是一个专门收集和展示B站"抽象视频"的排行榜工具。通过用户的互动行为（点亮问号）来收集数据，并结合弹幕同步功能，为用户提供一个有趣的内容发现平台。

### 🎯 解决的问题
- 缺乏对"抽象"视频的系统性标记与聚合展示
- 用户表达疑惑或调侃（如发送"？"弹幕）的行为未被记录与利用
- 没有跨平台可用的专用客户端来统一实现该功能

---

## ✨ 功能特色

### 问号点亮
在B站视频工具栏增加专属"问号"按钮，如果你觉得这个视频值得你发一个"？"，那么就点亮它。

### 弹幕联动
点亮问号时，自动在当前视频发送一条内容为"？"的弹幕，实现行为同步。

### 实时榜单
点击插件图标，即可查看今日、本周及本月最"抽象"的视频排行。

### 跨平台支持
基于Qt类UI设计，保证在Windows、macOS、Linux等系统上均可运行。

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- PyQt6
- pip / PDM

### 安装步骤

1. 克隆项目：
   ```bash
   git clone https://github.com/your-username/bili-qml-desktop.git
   cd bili-qml-desktop
   ```

2. 安装PDM依赖管理器：
   ```bash
   pip install pdm
   ```

3. 安装项目依赖：
   ```bash
   pdm install
   ```

4. 运行项目：
   ```bash
   pdm run python src/my_pyqt_app/__main__.py
   ```

---

## 🔧 项目结构

```
bili-qml-desktop/
├── src/
│   └── my_pyqt_app/
│       ├── models/           # 数据模型层
│       │   └── bilibili_api.py
│       ├── ui/               # 界面定义
│       │   └── ui_main_window.py
│       ├── views/            # 视图控制器
│       │   └── main_window.py
│       ├── __init__.py
│       └── __main__.py       # 主程序入口
├── README.md                 # 项目说明文档
└── pyproject.toml           # 项目配置文件
```

### 核心组件
- [views/main_window.py](./src/my_pyqt_app/views/main_window.py) - 负责业务逻辑调度
- [ui/ui_main_window.py](./src/my_pyqt_app/ui/ui_main_window.py) - 提供可视化界面元素绑定
- [models/bilibili_api.py](./src/my_pyqt_app/models/bilibili_api.py) - 处理与B站API通信

---

## 📝 贡献指南

欢迎提交Issue和Pull Request来帮助我们改进项目！

---

## 📄 许可证

本项目采用 [GPL-3.0](./LICENSE) 许可证。

---

## 版本历史

### v1.0.1 (2026-01-26)
- 优化UI显示效果，修复表格选中时文字颜色问题
- 改进网络错误处理机制，增强稳定性
- 优化标题显示逻辑，保持主标题始终为"B站问号榜"
- 完善README文档内容

### v1.0.0
- 实现基本的排行榜功能
- 添加日榜、周榜、月榜切换
- 实现基础UI界面
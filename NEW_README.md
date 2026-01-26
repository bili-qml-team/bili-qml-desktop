<h1 align="center">B站问号榜 (Bilibili Question-Mark Leaderboard)</h1>

<p align="center">
  <strong>分享抽象的视频，自动同步弹幕，打造Bilibili的抽象视频排行榜。</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/qt-pyqt6-green" alt="Qt Framework">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License">
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
- pip / Poetry

### 安装步骤

1. 克隆项目：
   ```bash
   git clone https://github.com/your-username/bili-qml-desktop.git
   cd bili-qml-desktop
   ```

2. （推荐）安装Poetry依赖管理器：
   ```bash
   pip install poetry
   ```

3. 安装项目依赖：
   ```bash
   # 使用Poetry
   poetry install
   
   # 或者使用pip
   pip install -r requirements.txt
   ```

4. 运行项目：
   ```bash
   python -m src.my_pyqt_app
   ```

---

## 🔧 开发指南

### 项目结构
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
├── NEW_README.md             # 项目说明文档
├── README.md                 # 原始文档
└── pyproject.toml           # 项目配置文件
```

### 核心组件
- [views/main_window.py](./src/my_pyqt_app/views/main_window.py) - 负责业务逻辑调度
- [ui/ui_main_window.py](./src/my_pyqt_app/ui/ui_main_window.py) - 提供可视化界面元素绑定
- [models/bilibili_api.py](./src/my_pyqt_app/models/bilibili_api.py) - 处理与B站API通信

### API接口
项目通过自定义后端API获取排行榜数据：
- 日榜：`https://bili-qml.bydfk.com/api/leaderboard?range=daily&type=1`
- 周榜：`https://bili-qml.bydfk.com/api/leaderboard?range=weekly&type=1`
- 月榜：`https://bili-qml.bydfk.com/api/leaderboard?range=monthly&type=1`

---

## 📊 数据展示

应用提供以下数据展示：

| 列名 | 描述 |
|------|------|
| 排名 | 视频在榜单中的位置 |
| 视频标题 | 视频的标题名称 |
| UP主 | 视频发布者昵称 |
| 播放量 | 视频播放次数（带单位） |
| 弹幕数 | 视频弹幕总数（带单位） |
| 点赞数 | 视频获得点赞数（带单位） |
| 时长 | 视频播放时长 |

---

## 🛠️ 技术栈

- **语言**: Python 3.8+
- **GUI框架**: PyQt6
- **网络请求**: requests
- **项目管理**: Poetry (pyproject.toml)
- **UI设计**: Qt Designer

---

## 🤝 贡献

欢迎提交Issue和Pull Request来帮助改进项目！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](./LICENSE) 文件。

---

## 📞 联系方式

如有任何问题或建议，请通过 GitHub Issues 联系我们。

---

<p align="center">
  <em>享受抽象文化，发现更多有趣的视频！</em>
</p>
#!/usr/bin/env python3
"""
B站问号榜 - 主程序入口
"""
import sys
import os
import logging
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
from ui.ui_main_window import Ui_BilibiliRankWindow as MainWindow

def setup_logging():
    """配置日志系统"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bilibili_rank.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main():
    """主函数"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # 创建应用实例
        app = QApplication(sys.argv)
        app.setApplicationName("B站问号榜")
        app.setApplicationVersion("1.0.0")
        
        # 创建主窗口
        logger.info("启动B站问号榜应用")
        # Ui_BilibiliRankWindow is a generated UI class; instantiate a QMainWindow and apply the UI to it.
        window = QMainWindow()
        ui = MainWindow()
        ui.setupUi(window)
        
        # 显示窗口
        window.show()
        
        # 延迟加载初始数据（避免界面卡顿）
        QTimer.singleShot(100, getattr(ui, "load_initial_data", lambda: None))
        
        # 运行应用
        return_code = app.exec()
        logger.info("应用正常退出")
        return return_code
        
    except Exception as e:
        logger.error(f"应用启动失败: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
from PyQt6.QtWidgets import QMainWindow, QWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from my_pyqt_app.ui.ui_main_window import Ui_BilibiliRankWindow as Ui_MainWindow
from my_pyqt_app.models.bilibili_api import BilibiliAPIManager
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.current_rank_type = "daily"
        self.api_manager = None
        # 初始化UI（把生成的 QWidget 作为 central widget）
        self.ui = Ui_MainWindow()
        self._central = QWidget()
        self.setCentralWidget(self._central)
        self.ui.setupUi(self._central)

        # 可选：确保主窗口标题（UI 也会设置，但显式设置不会有坏处）
        self.setWindowTitle("B站问号榜")

        # 设置初始状态
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """初始化界面设置"""
        # 设置表格属性
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels([
            "排名", "视频标题", "UP主", "播放量", "弹幕数", "点赞数", "时长"
        ])
        
        # 设置列宽策略
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # 排名
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # 标题自适应
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # UP主
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # 播放量
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # 弹幕数
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # 点赞数
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # 时长
        
        # 隐藏进度条和错误标签
        self.ui.progressBar.setVisible(False)
        self.ui.errorLabel.setVisible(False)
        
    def setup_connections(self):
        """连接信号和槽"""
        # 标签按钮点击事件
        self.ui.dailyButton.clicked.connect(lambda: self.switch_rank("daily"))
        self.ui.weeklyButton.clicked.connect(lambda: self.switch_rank("weekly"))
        self.ui.monthlyButton.clicked.connect(lambda: self.switch_rank("monthly"))
        # self.ui.realtimeButton.clicked.connect(lambda: self.switch_rank("realtime"))
        
        # 刷新按钮
        self.ui.refreshButton.clicked.connect(self.load_rank_data)
        
        # 设置自动刷新定时器（5分钟）
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
        self.refresh_timer.start(300000)
        
    def switch_rank(self, rank_type):
        """切换榜单类型"""
        if self.current_rank_type == rank_type:
            return
            
        self.current_rank_type = rank_type
        self.logger.info(f"切换到{rank_type}榜")
        
        # 更新按钮样式
        self.update_tab_style(rank_type)
        
        # 更新标题
        rank_names = {"daily": "日榜", "weekly": "周榜", "monthly": "月榜", "realtime": "实时榜"}
        self.ui.titleLabel.setText(f"B站{rank_names[rank_type]}问号榜")
        
        # 加载数据
        self.load_rank_data()
        
    def update_tab_style(self, active_tab):
        """更新标签按钮样式"""
        tabs = {
            "daily": self.ui.dailyButton,
            "weekly": self.ui.weeklyButton,
            "monthly": self.ui.monthlyButton,
            # "realtime": self.ui.realtimeButton
        }
        
        for tab_name, button in tabs.items():
            if tab_name == active_tab:
                button.setStyleSheet("""
                    QPushButton {
                        color: #00a1d6; 
                        font-size: 16px; 
                        font-weight: bold;
                        text-decoration: underline;
                        background: transparent; 
                        border: none;
                        padding: 5px 10px;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        color: #666666; 
                        font-size: 16px; 
                        background: transparent; 
                        border: none;
                        padding: 5px 10px;
                    }
                """)
    
    def load_initial_data(self):
        """加载初始数据"""
        self.load_rank_data()
    
    def load_rank_data(self):
        """加载榜单数据"""
        self.logger.info(f"开始加载{self.current_rank_type}榜数据")
        
        # 显示加载状态
        self.ui.errorLabel.setVisible(False)
        self.ui.tableWidget.setVisible(True)
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setValue(0)
        
        # 显示加载中的表格行
        self.ui.tableWidget.setRowCount(1)
        loading_item = QTableWidgetItem("加载中...")
        loading_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tableWidget.setItem(0, 0, loading_item)
        self.ui.tableWidget.setSpan(0, 0, 1, 7)
        
        # 启动API请求
        self.api_manager = BilibiliAPIManager(self.current_rank_type)
        self.api_manager.data_received.connect(self.display_rank_data)
        self.api_manager.error_occurred.connect(self.handle_api_error)
        self.api_manager.progress_updated.connect(self.ui.progressBar.setValue)
        self.api_manager.start()
    
    def display_rank_data(self, data):
        """显示榜单数据"""
        try:
            self.ui.progressBar.setVisible(False)
            
            if not data:
                self.show_empty_data()
                return
                
            # 清除加载状态
            self.ui.tableWidget.clearSpans()
            self.ui.tableWidget.setRowCount(len(data))
            
            # 填充数据
            for row, item in enumerate(data):
                self.add_table_row(row, item)
            
            # 更新状态信息
            self.update_status_info(len(data))
            self.logger.info(f"成功加载{len(data)}条数据")
            
        except Exception as e:
            self.logger.error(f"数据显示错误: {str(e)}")
            self.handle_api_error(f"数据处理错误: {str(e)}")
    
    def add_table_row(self, row, item):
        """添加表格行数据"""
        # 排名
        rank_item = QTableWidgetItem(str(item['rank']))
        rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tableWidget.setItem(row, 0, rank_item)
        
        # 视频标题
        title_item = QTableWidgetItem(item['title'])
        title_item.setToolTip(item['title'])
        self.ui.tableWidget.setItem(row, 1, title_item)
        
        # UP主
        up_item = QTableWidgetItem(item['up'])
        self.ui.tableWidget.setItem(row, 2, up_item)
        
        # 播放量
        play_item = QTableWidgetItem(item['play'])
        play_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.ui.tableWidget.setItem(row, 3, play_item)
        
        # 弹幕数
        danmaku_item = QTableWidgetItem(item['danmaku'])
        danmaku_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.ui.tableWidget.setItem(row, 4, danmaku_item)
        
        # 点赞数
        like_item = QTableWidgetItem(item['like'])
        like_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.ui.tableWidget.setItem(row, 5, like_item)
        
        # 时长
        duration_item = QTableWidgetItem(item['duration'])
        duration_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tableWidget.setItem(row, 6, duration_item)
        
        # 前三名特殊样式
        if item['rank'] <= 3:
            for col in range(7):
                self.ui.tableWidget.item(row, col).setBackground(QColor(255, 248, 225))
    
    def update_status_info(self, data_count):
        """更新状态栏信息"""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.updateLabel.setText(f"最后更新: {current_time}")
        self.ui.countLabel.setText(f"数据数量: {data_count}")
    
    def show_empty_data(self):
        """显示空数据状态"""
        self.ui.tableWidget.setRowCount(1)
        empty_item = QTableWidgetItem("暂无数据")
        empty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.ui.tableWidget.setItem(0, 0, empty_item)
        self.ui.tableWidget.setSpan(0, 0, 1, 7)
        self.update_status_info(0)
    
    def handle_api_error(self, error_msg):
        """处理API错误"""
        self.ui.progressBar.setVisible(False)
        self.ui.tableWidget.setVisible(False)
        self.ui.errorLabel.setText(f"获取{self.current_rank_type}榜失败: {error_msg}")
        self.ui.errorLabel.setVisible(True)
        self.update_status_info(0)
        self.logger.error(f"API错误: {error_msg}")
        
        # 显示错误对话框
        QMessageBox.warning(self, "数据加载失败", error_msg)
    
    def auto_refresh(self):
        """自动刷新数据"""
        if hasattr(self, 'last_update_time'):
            self.logger.info("执行自动刷新")
            self.load_rank_data()
    
    def closeEvent(self, event):
        """重写关闭事件"""
        self.logger.info("正在关闭应用...")
        if self.api_manager and self.api_manager.isRunning():
            self.api_manager.terminate()
            self.api_manager.wait()
        event.accept()
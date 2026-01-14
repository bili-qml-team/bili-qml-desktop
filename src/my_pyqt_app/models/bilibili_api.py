import requests
import random
from PyQt6.QtCore import QThread, pyqtSignal

class BilibiliAPIManager(QThread):
    """B站API数据获取线程"""
    data_received = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)
    
    def __init__(self, rank_type="daily"):
        super().__init__()
        self.rank_type = rank_type
        self.api_urls = {
            "daily": "https://api.bilibili.com/x/web-interface/popular",
            "weekly": "https://api.bilibili.com/x/web-interface/ranking/v2",
            "monthly": "https://api.bilibili.com/x/web-interface/ranking/v2"
        }
        
    def get_headers(self):
        """获取随机User-Agent头部信息"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
        ]
        return {
            'User-Agent': random.choice(user_agents),
            'Referer': 'https://www.bilibili.com/',
            'Origin': 'https://www.bilibili.com'
        }
    
    def format_number(self, num):
        """格式化数字显示"""
        if num >= 10000:
            return f"{num/10000:.1f}万"
        return str(num)
    
    def run(self):
        try:
            self.progress_updated.emit(10)
            
            # 构建请求参数
            params = {}
            if self.rank_type in ["weekly", "monthly"]:
                params = {'rid': 0, 'type': 'all'}
            
            self.progress_updated.emit(30)
            
            # 发送API请求
            response = requests.get(
                self.api_urls[self.rank_type], 
                params=params,
                headers=self.get_headers(),
                timeout=10
            )
            
            self.progress_updated.emit(60)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('code') == 0:
                    rank_list = data['data']['list']
                    processed_data = []
                    
                    for i, item in enumerate(rank_list):
                        rank_info = {
                            'rank': i + 1,
                            'title': item.get('title', '未知标题'),
                            'up': item['owner']['name'],
                            'play': self.format_number(item['stat']['view']),
                            'danmaku': self.format_number(item['stat']['danmaku']),
                            'like': self.format_number(item['stat']['like']),
                            'duration': self.format_duration(item.get('duration', 0))
                        }
                        processed_data.append(rank_info)
                    
                    self.progress_updated.emit(90)
                    self.data_received.emit(processed_data)
                else:
                    self.error_occurred.emit(f"API返回错误: {data.get('message', '未知错误')}")
            else:
                self.error_occurred.emit(f"HTTP错误: {response.status_code}")
                
        except Exception as e:
            self.error_occurred.emit(f"网络请求失败: {str(e)}")
        finally:
            self.progress_updated.emit(100)
    
    def format_duration(self, seconds):
        """格式化视频时长"""
        if not seconds:
            return "未知"
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
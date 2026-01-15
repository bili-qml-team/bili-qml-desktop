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
            # "realtime": "https://bili-qml.bydfk.com/api/leaderboard?range=realtime&type=1",
            "daily": "https://bili-qml.bydfk.com/api/leaderboard?range=daily&type=1",
            "weekly": "https://bili-qml.bydfk.com/api/leaderboard?range=weekly&type=1",
            "monthly": "https://bili-qml.bydfk.com/api/leaderboard?range=monthly&type=1"
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
            
            # 发送API请求到自定义后端
            response = requests.get(
                self.api_urls[self.rank_type], 
                headers=self.get_headers(),
                timeout=10
            )
            
            self.progress_updated.emit(30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    rank_list = data['list']
                    processed_data = []
                    total = len(rank_list)
                    
                    for i, item in enumerate(rank_list):
                        bvid = item['bvid']
                        title = item.get('title', '未知标题')
                        
                        # 获取视频详情
                        try:
                            detail_response = requests.get(
                                f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
                                headers=self.get_headers(),
                                timeout=10
                            )
                            
                            if detail_response.status_code == 200:
                                detail_data = detail_response.json()
                                if detail_data.get('code') == 0:
                                    video_data = detail_data['data']
                                    rank_info = {
                                        'rank': i + 1,
                                        'title': title,
                                        'up': video_data['owner']['name'],
                                        'play': self.format_number(video_data['stat']['view']),
                                        'danmaku': self.format_number(video_data['stat']['danmaku']),
                                        'like': self.format_number(video_data['stat']['like']),
                                        'duration': self.format_duration(video_data.get('duration', 0))
                                    }
                                else:
                                    rank_info = {
                                        'rank': i + 1,
                                        'title': title,
                                        'up': '未知',
                                        'play': '0',
                                        'danmaku': '0',
                                        'like': '0',
                                        'duration': '未知'
                                    }
                            else:
                                rank_info = {
                                    'rank': i + 1,
                                    'title': title,
                                    'up': '未知',
                                    'play': '0',
                                    'danmaku': '0',
                                    'like': '0',
                                    'duration': '未知'
                                }
                        except Exception as e:
                            rank_info = {
                                'rank': i + 1,
                                'title': title,
                                'up': '未知',
                                'play': '0',
                                'danmaku': '0',
                                'like': '0',
                                'duration': '未知'
                            }
                        
                        processed_data.append(rank_info)
                        self.progress_updated.emit(30 + int(60 * (i + 1) / total))
                    
                    self.progress_updated.emit(90)
                    self.data_received.emit(processed_data)
                else:
                    self.error_occurred.emit("API返回失败")
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
"""
窗口管理器 - 获取游戏窗口句柄和信息
"""
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

class WindowManager:
    """游戏窗口管理器"""
    
    @staticmethod
    def get_window_by_title(title_keyword):
        """
        根据标题关键词查找窗口
        :param title_keyword: 窗口标题关键词
        :return: 窗口句柄（hwnd）
        """
        hwnd = user32.FindWindowW(None, title_keyword)
        if hwnd == 0:
            # 尝试枚举所有窗口查找
            hwnd = WindowManager._enum_windows_by_title(title_keyword)
        return hwnd
    
    @staticmethod
    def _enum_windows_by_title(title_keyword):
        """枚举所有窗口查找匹配标题"""
        result = {'hwnd': 0}
        
        def callback(hwnd, lparam):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                if title_keyword. lower() in buff.value.lower():
                    result['hwnd'] = hwnd
                    return False  # 停止枚举
            return True
        
        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        user32.EnumWindows(WNDENUMPROC(callback), 0)
        return result['hwnd']
    
    @staticmethod
    def get_window_rect(hwnd):
        """
        获取窗口位置和大小
        :return: (x, y, width, height)
        """
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        return (rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)
    
    @staticmethod
    def get_window_title(hwnd):
        """获取窗口标题"""
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff. value
    
    @staticmethod
    def activate_window(hwnd):
        """激活窗口（置于前台）"""
        user32.SetForegroundWindow(hwnd)
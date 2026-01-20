"""
窗口管理器 - 获取游戏窗口句柄和信息
"""
import ctypes
from ctypes import wintypes
from typing import List, Tuple, Optional

user32 = ctypes.windll.user32

class WindowInfo:
    """窗口信息类"""
    def __init__(self, hwnd: int, title: str, class_name: str):
        self.hwnd = hwnd
        self.title = title
        self.class_name = class_name
        self.rect = None
    
    def __str__(self):
        return f"[{self.hwnd}] {self.title} ({self.class_name})"

class WindowManager:
    """游戏窗口管理器"""
    
    def __init__(self):
        self.current_hwnd = None
        self.current_window_info = None
    
    @staticmethod
    def get_all_windows() -> List[WindowInfo]:
        """
        枚举所有可见窗口
        : return: 窗口信息列表
        """
        windows = []
        
        def callback(hwnd, lparam):
            # 只获取可见窗口
            if user32.IsWindowVisible(hwnd):
                # 获取窗口标题
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    title_buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, title_buff, length + 1)
                    title = title_buff.value
                    
                    # 获取窗口类名
                    class_buff = ctypes.create_unicode_buffer(256)
                    user32.GetClassNameW(hwnd, class_buff, 256)
                    class_name = class_buff.value
                    
                    # 过滤掉一些系统窗口
                    if title and title.strip():
                        windows.append(WindowInfo(hwnd, title, class_name))
            return True
        
        # 枚举所有顶级窗口
        WNDENUMPROC = ctypes. WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        user32.EnumWindows(WNDENUMPROC(callback), 0)
        
        return windows
    
    @staticmethod
    def get_window_by_title(title_keyword: str) -> Optional[int]:
        """
        根据标题关键词查找窗口
        :param title_keyword: 窗口标题关键词
        :return: 窗口句柄（hwnd）
        """
        windows = WindowManager.get_all_windows()
        for window in windows:
            if title_keyword.lower() in window.title.lower():
                return window.hwnd
        return None
    
    @staticmethod
    def get_window_rect(hwnd: int) -> Tuple[int, int, int, int]:
        """
        获取窗口位置和大小
        :return: (x, y, width, height)
        """
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        return (rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)
    
    @staticmethod
    def get_client_rect(hwnd: int) -> Tuple[int, int, int, int]:
        """
        获取窗口客户区大小（不含标题栏和边框）
        :return: (x, y, width, height)
        """
        rect = wintypes.RECT()
        user32.GetClientRect(hwnd, ctypes. byref(rect))
        return (rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)
    
    @staticmethod
    def get_window_title(hwnd: int) -> str:
        """获取窗口标题"""
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return ""
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff. value
    
    @staticmethod
    def is_window_valid(hwnd: int) -> bool:
        """检查窗口句柄是否有效"""
        return user32.IsWindow(hwnd) != 0
    
    @staticmethod
    def activate_window(hwnd: int) -> bool:
        """
        激活窗口（置于前台）
        :return: 是否成功
        """
        if not WindowManager.is_window_valid(hwnd):
            return False
        
        # 如果窗口最小化，先恢复
        if user32.IsIconic(hwnd):
            user32.ShowWindow(hwnd, 9)  # SW_RESTORE
        
        user32.SetForegroundWindow(hwnd)
        return True
    
    def select_window(self, hwnd: int) -> bool:
        """
        选择并绑定窗口
        : param hwnd: 窗口句柄
        :return:  是否成功
        """
        if not self.is_window_valid(hwnd):
            return False
        
        self.current_hwnd = hwnd
        title = self.get_window_title(hwnd)
        class_buff = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, class_buff, 256)
        class_name = class_buff.value
        
        self.current_window_info = WindowInfo(hwnd, title, class_name)
        self.current_window_info.rect = self.get_window_rect(hwnd)
        
        return True
    
    def get_current_window_info(self) -> Optional[WindowInfo]: 
        """获取当前选中的窗口信息"""
        if self.current_hwnd and self.is_window_valid(self.current_hwnd):
            # 更新窗口位置信息
            self.current_window_info.rect = self.get_window_rect(self.current_hwnd)
            return self.current_window_info
        return None
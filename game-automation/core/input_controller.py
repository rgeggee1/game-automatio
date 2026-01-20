"""
输入控制器 - 支持多种输入方式
"""
import win32api
import win32con
import win32gui
import time
from typing import Tuple, Optional

class InputController:
    """
    输入控制器 - 支持鼠标和键盘输入
    支持多种实现方式：PostMessage, SendMessage, SendInput
    """
    
    def __init__(self, hwnd):
        """
        初始化输入控制器
        
        : param hwnd: 目标窗口句柄
        """
        self.hwnd = hwnd
        
        # 虚拟键码映射
        self.VK_MAP = {
            # 功能键
            'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73,
            'F5': 0x74, 'F6':  0x75, 'F7': 0x76, 'F8': 0x77,
            'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B,
            
            # 数字键
            '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
            '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
            
            # 字母键
            'A': 0x41, 'B':  0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45,
            'F': 0x46, 'G': 0x47, 'H': 0x48, 'I':  0x49, 'J': 0x4A,
            'K': 0x4B, 'L': 0x4C, 'M':  0x4D, 'N': 0x4E, 'O': 0x4F,
            'P': 0x50, 'Q':  0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54,
            'U': 0x55, 'V': 0x56, 'W': 0x57, 'X':  0x58, 'Y': 0x59,
            'Z': 0x5A,
            
            # 特殊键
            'SPACE': 0x20,
            'ENTER': 0x0D,
            'ESC': 0x1B,
            'TAB': 0x09,
            'SHIFT': 0x10,
            'CTRL': 0x11,
            'ALT': 0x12,
            
            # 方向键
            'LEFT': 0x25,
            'UP': 0x26,
            'RIGHT': 0x27,
            'DOWN': 0x28,
        }
    
    def get_vk_code(self, key):
        """
        获取虚拟键码
        
        :param key:  键名或虚拟键码
        :return: 虚拟键码
        """
        if isinstance(key, int):
            return key
        
        key_upper = key.upper()
        if key_upper in self.VK_MAP:
            return self. VK_MAP[key_upper]
        
        # 如果是单字符，直接转换
        if len(key) == 1:
            return ord(key. upper())
        
        raise ValueError(f"Unknown key: {key}")
    
    # ==================== 键盘输入方法 ====================
    
    def send_key(self, key, duration=0.05):
        """
        发送按键到窗口 - 使用 PostMessage
        
        :param key: 键名或虚拟键码
        :param duration: 按键持续时间（秒）
        """
        vk_code = self.get_vk_code(key)
        
        # 按下
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code, 0)
        time.sleep(duration)
        
        # 释放
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, vk_code, 0)
        time.sleep(0.05)
    
    def send_key_direct(self, key, duration=0.05):
        """
        发送按键 - 使用 SendMessage (同步)
        
        :param key: 键名或虚拟键码
        :param duration: 按键持续时间（秒）
        """
        vk_code = self.get_vk_code(key)
        
        # 按下
        win32gui.SendMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code, 0)
        time.sleep(duration)
        
        # 释放
        win32gui.SendMessage(self.hwnd, win32con.WM_KEYUP, vk_code, 0)
        time.sleep(0.05)
    
    def send_char(self, char):
        """
        发送字符（支持中文）
        
        :param char: 字符
        """
        for c in char:
            win32api.PostMessage(self. hwnd, win32con.WM_CHAR, ord(c), 0)
            time.sleep(0.02)
    
    def send_key_combo(self, *keys, duration=0.05):
        """
        发送组合键（如 Ctrl+C）
        
        :param keys: 键序列，如 ('CTRL', 'C')
        : param duration: 按键持续时间
        """
        vk_codes = [self.get_vk_code(k) for k in keys]
        
        # 按下所有键
        for vk in vk_codes:
            win32api.PostMessage(self. hwnd, win32con.WM_KEYDOWN, vk, 0)
            time.sleep(0.02)
        
        time.sleep(duration)
        
        # 释放所有键（逆序）
        for vk in reversed(vk_codes):
            win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, vk, 0)
            time.sleep(0.02)
    
    # ==================== 鼠标输入方法 ====================
    
    def click_input(self, x, y, restore_cursor=True, hover_time=0.3, click_duration=0.1):
        """
        在指定位置点击鼠标左键 - 增强版
        
        :param x: 屏幕坐标 x
        :param y: 屏幕坐标 y
        :param restore_cursor: 是否恢复鼠标位置
        :param hover_time: 鼠标移动后停留时间（秒） - 让游戏识别悬停
        :param click_duration: 鼠标按下持续时间（秒）
        """
        # 保存原始鼠标位置
        if restore_cursor:
            original_pos = win32api.GetCursorPos()
        
        # 1. 移动鼠标到目标位置
        win32api. SetCursorPos((x, y))
        
        # 2. 停留一段时间（让游戏识别到鼠标悬停）
        time.sleep(hover_time)
        
        # 3. 按下鼠标左键
        win32api.mouse_event(win32con. MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        
        # 4. 保持按下状态一段时间
        time.sleep(click_duration)
        
        # 5. 释放鼠标左键
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        
        # 6. 点击后再停留一小段时间（确保游戏处理完事件）
        time.sleep(0.15)
        
        # 7. 恢复鼠标位置
        if restore_cursor:
            time.sleep(0.1)
            win32api.SetCursorPos(original_pos)
    
    def click_at_client(self, x, y, button='left'):
        """
        在客户区坐标点击 - 使用 PostMessage
        
        :param x: 客户区坐标 x
        :param y: 客户区坐标 y
        :param button: 'left' 或 'right'
        """
        lparam = win32api.MAKELONG(x, y)
        
        if button == 'left':
            win32api.PostMessage(self.hwnd, win32con. WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
            time.sleep(0.05)
            win32api.PostMessage(self.hwnd, win32con. WM_LBUTTONUP, 0, lparam)
        elif button == 'right':
            win32api.PostMessage(self.hwnd, win32con. WM_RBUTTONDOWN, win32con.MK_RBUTTON, lparam)
            time.sleep(0.05)
            win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONUP, 0, lparam)
    
    def double_click(self, x, y, restore_cursor=True):
        """
        双击
        
        :param x: 屏幕坐标 x
        :param y: 屏幕坐标 y
        :param restore_cursor: 是否恢复鼠标位置
        """
        if restore_cursor:
            original_pos = win32api.GetCursorPos()
        
        win32api.SetCursorPos((x, y))
        time.sleep(0.1)
        
        # 第一次点击
        win32api.mouse_event(win32con. MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        
        time.sleep(0.1)
        
        # 第二次点击
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        
        if restore_cursor:
            time. sleep(0.1)
            win32api.SetCursorPos(original_pos)
    
    def right_click(self, x, y, restore_cursor=True):
        """
        右键点击
        
        :param x:  屏幕坐标 x
        :param y:  屏幕坐标 y
        :param restore_cursor: 是否恢复鼠标位置
        """
        if restore_cursor: 
            original_pos = win32api.GetCursorPos()
        
        win32api. SetCursorPos((x, y))
        time.sleep(0.1)
        
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        time.sleep(0.05)
        win32api.mouse_event(win32con. MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
        
        if restore_cursor:
            time. sleep(0.1)
            win32api.SetCursorPos(original_pos)
    
    def move_mouse(self, x, y):
        """
        移动鼠标到指定位置
        
        :param x:  屏幕坐标 x
        :param y:  屏幕坐标 y
        """
        win32api.SetCursorPos((x, y))
    
    # ==================== 辅助方法 ====================
    
    def screen_to_client(self, x, y):
        """
        屏幕坐标转客户区坐标
        
        :param x: 屏幕坐标 x
        :param y: 屏幕坐标 y
        : return: (client_x, client_y)
        """
        point = win32gui.ScreenToClient(self. hwnd, (x, y))
        return point
    
    def client_to_screen(self, x, y):
        """
        客户区坐标转屏幕坐标
        
        : param x: 客户区坐标 x
        :param y: 客户区坐标 y
        :return:  (screen_x, screen_y)
        """
        point = win32gui.ClientToScreen(self.hwnd, (x, y))
        return point
    
    def get_client_rect(self):
        """
        获取窗口客户区大小
        
        :return:  (left, top, right, bottom)
        """
        rect = win32gui.GetClientRect(self. hwnd)
        return rect
    
    def activate_window(self):
        """
        激活窗口（使其获得焦点）
        """
        try:
            win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self.hwnd)
            time.sleep(0.1)
            return True
        except Exception as e: 
            print(f"激活窗口失败: {e}")
            return False
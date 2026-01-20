"""
输入控制器 - 完美工作版
✅ F1-F4: SendMessageW 到子窗口
✅ 数字1-6: PostMessageW 到子窗口
✅ 字母M: SendMessageW 主窗口
✅ 鼠标:  SendInput + 光标恢复
"""
import ctypes
from ctypes import wintypes
import time
import win32gui
import win32api

user32 = ctypes.windll.user32

# Windows消息常量
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

# SendInput 常量（仅用于鼠标）
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUT_UNION)
    ]

class InputController:
    """反检测输入控制器 - 完美版"""
    
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.update_window_rect()
        self.debug = False
    
    def update_window_rect(self):
        """更新窗口位置信息"""
        rect = win32gui.GetWindowRect(self.hwnd)
        self.window_x = rect[0]
        self.window_y = rect[1]
        
        client_rect = win32gui.GetClientRect(self.hwnd)
        point = win32gui.ClientToScreen(self.hwnd, (0, 0))
        self.client_x = point[0]
        self.client_y = point[1]
    
    def is_function_key(self, vk_code):
        """判断是否是功能键（F1-F12）"""
        return 0x70 <= vk_code <= 0x7B
    
    def is_number_key(self, vk_code):
        """判断是否是数字键（0-9）"""
        return 0x30 <= vk_code <= 0x39
    
    def send_to_children_sync(self, vk_code, lparam_down, lparam_up, hold_time):
        """
        发送到所有子窗口 - 同步方式 (SendMessageW)
        用于：F1-F4
        """
        def enum_child_callback(hwnd, lparam):
            user32.SendMessageW(hwnd, WM_KEYDOWN, vk_code, lparam_down)
            time.sleep(hold_time / 3)
            user32.SendMessageW(hwnd, WM_KEYUP, vk_code, lparam_up)
            return True
        
        EnumChildProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        user32.EnumChildWindows(self.hwnd, EnumChildProc(enum_child_callback), 0)
        
        # 同时发送到主窗口
        user32.SendMessageW(self.hwnd, WM_KEYDOWN, vk_code, lparam_down)
        time.sleep(hold_time)
        user32.SendMessageW(self.hwnd, WM_KEYUP, vk_code, lparam_up)
    
    def send_to_children_async(self, vk_code, lparam_down, lparam_up, hold_time):
        """
        发送到所有子窗口 - 异步方式 (PostMessageW)
        用于：数字键 1-6 ⭐
        """
        def enum_child_callback(hwnd, lparam):
            user32.PostMessageW(hwnd, WM_KEYDOWN, vk_code, lparam_down)
            time.sleep(hold_time / 3)
            user32.PostMessageW(hwnd, WM_KEYUP, vk_code, lparam_up)
            return True
        
        EnumChildProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        user32.EnumChildWindows(self.hwnd, EnumChildProc(enum_child_callback), 0)
        
        # 同时发送到主窗口
        user32.PostMessageW(self.hwnd, WM_KEYDOWN, vk_code, lparam_down)
        time.sleep(hold_time)
        user32.PostMessageW(self.hwnd, WM_KEYUP, vk_code, lparam_up)
    
    def send_key(self, vk_code, hold_time=0.05):
        """
        发送按键消息 - 智能选择最佳方法
        
        ✅ F1-F12: SendMessageW 到子窗口（同步）
        ✅ 数字0-9: PostMessageW 到子窗口（异步）⭐
        ✅ 字母等: SendMessageW 主窗口
        """
        scan_code = user32.MapVirtualKeyW(vk_code, 0)
        
        # 构造 lparam
        repeat_count = 1
        lparam_down = (repeat_count | (scan_code << 16))
        lparam_up = (repeat_count | (scan_code << 16) | 0xC0000000)
        
        if self.debug:
            print(f"🔍 发送按键:  VK=0x{vk_code:02X}, 扫描码=0x{scan_code:02X}")
        
        # 功能键 F1-F12: 使用 SendMessageW 到子窗口
        if self.is_function_key(vk_code):
            if self.debug:
                print(f"  → 功能键，SendMessageW 到所有子窗口...")
            self.send_to_children_sync(vk_code, lparam_down, lparam_up, hold_time)
        
        # 数字键 0-9: 使用 PostMessageW 到子窗口 ⭐
        elif self.is_number_key(vk_code):
            if self.debug:
                print(f"  → 数字键，PostMessageW 到所有子窗口...")
            self.send_to_children_async(vk_code, lparam_down, lparam_up, hold_time)
        
        # 其他按键:  直接发送到主窗口
        else: 
            if self.debug:
                print(f"  → 普通按键，SendMessageW 主窗口...")
            user32.SendMessageW(self. hwnd, WM_KEYDOWN, vk_code, lparam_down)
            time.sleep(hold_time)
            user32.SendMessageW(self.hwnd, WM_KEYUP, vk_code, lparam_up)
    
    def send_key_all_methods(self, vk_code, hold_time=0.05):
        """测试所有方法（保留用于调试）"""
        scan_code = user32.MapVirtualKeyW(vk_code, 0)
        
        print(f"\n{'='*70}")
        print(f"🧪 测试按键 VK=0x{vk_code:02X}, 扫描码=0x{scan_code:02X}")
        print(f"{'='*70}\n")
        
        lparam_down = (1 | (scan_code << 16))
        lparam_up = (1 | (scan_code << 16) | 0xC0000000)
        
        # 方法1: SendMessageW 到子窗口
        print("┌" + "─"*68 + "┐")
        print("│ [方法1] SendMessageW 到所有子窗口 (F1-F4 有效)                   │")
        print("└" + "─"*68 + "┘")
        
        child_count = [0]
        
        def enum_send(hwnd, lparam):
            child_count[0] += 1
            user32.SendMessageW(hwnd, WM_KEYDOWN, vk_code, lparam_down)
            time.sleep(hold_time / 3)
            user32.SendMessageW(hwnd, WM_KEYUP, vk_code, lparam_up)
            return True
        
        EnumChildProc1 = ctypes.WINFUNCTYPE(wintypes. BOOL, wintypes.HWND, wintypes.LPARAM)
        user32.EnumChildWindows(self.hwnd, EnumChildProc1(enum_send), 0)
        user32.SendMessageW(self. hwnd, WM_KEYDOWN, vk_code, lparam_down)
        time.sleep(hold_time)
        user32.SendMessageW(self.hwnd, WM_KEYUP, vk_code, lparam_up)
        
        print(f"  → 发送到 {child_count[0]} 个子窗口")
        print(f"  ✓ 完毕，等待 2 秒.. .\n")
        time.sleep(2.0)
        
        # 方法2: PostMessageW 到子窗口
        print("┌" + "─"*68 + "┐")
        print("│ [方法2] PostMessageW 到所有子窗口 ⭐ (数字键 有效)              │")
        print("└" + "─"*68 + "┘")
        
        child_count[0] = 0
        
        def enum_post(hwnd, lparam):
            child_count[0] += 1
            user32.PostMessageW(hwnd, WM_KEYDOWN, vk_code, lparam_down)
            time.sleep(hold_time / 3)
            user32.PostMessageW(hwnd, WM_KEYUP, vk_code, lparam_up)
            return True
        
        EnumChildProc2 = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        user32.EnumChildWindows(self.hwnd, EnumChildProc2(enum_post), 0)
        user32.PostMessageW(self.hwnd, WM_KEYDOWN, vk_code, lparam_down)
        time.sleep(hold_time)
        user32.PostMessageW(self. hwnd, WM_KEYUP, vk_code, lparam_up)
        
        print(f"  → 发送到 {child_count[0]} 个子窗口")
        print(f"  ✓ 完毕，等待 2 秒...\n")
        time.sleep(2.0)
        
        print("=" * 70)
        print("✅ 测试完毕！")
        print("=" * 70)
    
    def move_mouse(self, x, y):
        """移动鼠标"""
        user32.SetCursorPos(x, y)
    
    def click_input(self, x, y, button='left', delay=0.05, restore_cursor=True):
        """使用 SendInput 点击鼠标"""
        self.update_window_rect()
        
        if restore_cursor:
            original_pos = win32api.GetCursorPos()
        
        screen_x, screen_y = win32gui.ClientToScreen(self.hwnd, (x, y))
        user32.SetCursorPos(screen_x, screen_y)
        time.sleep(0.01)
        
        if button == 'left':
            down_flag = MOUSEEVENTF_LEFTDOWN
            up_flag = MOUSEEVENTF_LEFTUP
        else: 
            down_flag = MOUSEEVENTF_RIGHTDOWN
            up_flag = MOUSEEVENTF_RIGHTUP
        
        mouse_down = INPUT()
        mouse_down.type = INPUT_MOUSE
        mouse_down.union.mi.dx = 0
        mouse_down.union.mi.dy = 0
        mouse_down.union.mi.mouseData = 0
        mouse_down. union.mi.dwFlags = down_flag
        mouse_down. union.mi.time = 0
        mouse_down.union. mi.dwExtraInfo = None
        
        mouse_up = INPUT()
        mouse_up.type = INPUT_MOUSE
        mouse_up.union.mi.dx = 0
        mouse_up.union.mi.dy = 0
        mouse_up.union.mi.mouseData = 0
        mouse_up.union.mi.dwFlags = up_flag
        mouse_up.union.mi.time = 0
        mouse_up. union.mi.dwExtraInfo = None
        
        user32.SendInput(1, ctypes.byref(mouse_down), ctypes.sizeof(INPUT))
        time.sleep(delay)
        user32.SendInput(1, ctypes.byref(mouse_up), ctypes.sizeof(INPUT))
        
        if restore_cursor:
            time.sleep(0.01)
            user32.SetCursorPos(original_pos[0], original_pos[1])
    
    def click_input_at_screen_pos(self, screen_x, screen_y, button='left', delay=0.05, restore_cursor=True):
        """使用屏幕坐标点击"""
        if restore_cursor:
            original_pos = win32api.GetCursorPos()
        
        user32.SetCursorPos(screen_x, screen_y)
        time.sleep(0.01)
        
        if button == 'left':
            down_flag = MOUSEEVENTF_LEFTDOWN
            up_flag = MOUSEEVENTF_LEFTUP
        else: 
            down_flag = MOUSEEVENTF_RIGHTDOWN
            up_flag = MOUSEEVENTF_RIGHTUP
        
        mouse_down = INPUT()
        mouse_down.type = INPUT_MOUSE
        mouse_down.union.mi.dx = 0
        mouse_down.union.mi.dy = 0
        mouse_down.union.mi.mouseData = 0
        mouse_down.union.mi. dwFlags = down_flag
        mouse_down.union.mi. time = 0
        mouse_down.union.mi.dwExtraInfo = None
        
        mouse_up = INPUT()
        mouse_up.type = INPUT_MOUSE
        mouse_up. union.mi.dx = 0
        mouse_up.union. mi.dy = 0
        mouse_up.union.mi. mouseData = 0
        mouse_up.union.mi.dwFlags = up_flag
        mouse_up.union.mi.time = 0
        mouse_up.union.mi.dwExtraInfo = None
        
        user32.SendInput(1, ctypes.byref(mouse_down), ctypes.sizeof(INPUT))
        time.sleep(delay)
        user32.SendInput(1, ctypes.byref(mouse_up), ctypes.sizeof(INPUT))
        
        if restore_cursor:
            time. sleep(0.01)
            user32.SetCursorPos(original_pos[0], original_pos[1])
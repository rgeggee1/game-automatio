"""
屏幕截图模块 - 捕获游戏窗口画面（修复版）
"""
import ctypes
from ctypes import wintypes
import numpy as np
from PIL import Image
import win32gui
import win32ui
import win32con
import os

class ScreenCapture:
    """屏幕截图器"""
    
    def __init__(self, hwnd):
        """
        初始化截图器
        : param hwnd: 窗口句柄
        """
        self.hwnd = hwnd
        self.update_window_size()
    
    def update_window_size(self):
        """更新窗口大小"""
        try:
            rect = win32gui.GetClientRect(self.hwnd)
            self.width = rect[2]
            self.height = rect[3]
        except Exception as e:
            print(f"⚠️ 更新窗口大小失败: {e}")
            self.width = 800
            self.height = 600
    
    def capture(self, region=None):
        """
        截取窗口画面（后台截图，不影响用户操作）
        :param region:  截取区域 (x, y, width, height)，None表示全屏
        : return: PIL Image 对象
        """
        try:
            # 获取窗口设备上下文
            hwndDC = win32gui.GetWindowDC(self.hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            # 确定截图区域
            if region is None:
                x, y = 0, 0
                width, height = self.width, self.height
            else:
                x, y, width, height = region
            
            # 创建位图对象
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)
            
            # 截图到位图
            result = saveDC.BitBlt((0, 0), (width, height), mfcDC, (x, y), win32con.SRCCOPY)
            
            # 转换为PIL Image
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            
            img = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            
            # 清理资源
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwndDC)
            
            return img
            
        except Exception as e:
            print(f"❌ 截图失败:  {e}")
            raise
    
    def capture_to_numpy(self, region=None):
        """
        截取窗口并转换为numpy数组（用于OpenCV处理）
        :param region:  截取区域
        :return: numpy数组 (BGR格式)
        """
        img = self.capture(region)
        # PIL是RGB，OpenCV是BGR，需要转换
        return np.array(img)[: , :, ::-1]. copy()
    
    def save_screenshot(self, filename, region=None):
        """
        保存截图到文件
        :param filename: 文件名
        :param region:  截取区域
        """
        try:
            # 确保文件扩展名正确
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                filename = filename + '.png'
            
            # 获取截图
            img = self.capture(region)
            
            # 确保目录存在
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # 保存图片
            img.save(filename, 'PNG')
            
            print(f"✅ 截图已保存:  {filename} ({img.width}x{img.height})")
            return filename
            
        except Exception as e:
            error_msg = f"保存截图失败: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
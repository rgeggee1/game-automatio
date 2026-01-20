"""
增强版截图模块 - 支持 DirectX/OpenGL 游戏
"""
import numpy as np
from PIL import Image
import win32gui
import win32ui
import win32con
from ctypes import windll
import time

class ScreenCaptureAdvanced:
    """支持 DirectX 游戏的截图器"""
    
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.update_window_size()
    
    def update_window_size(self):
        """更新窗口大小"""
        try:
            # 获取窗口矩形
            rect = win32gui.GetWindowRect(self. hwnd)
            self.left = rect[0]
            self.top = rect[1]
            self.right = rect[2]
            self.bottom = rect[3]
            self.width = self.right - self.left
            self.height = self.bottom - self.top
            
            # 获取客户区大小
            client_rect = win32gui.GetClientRect(self.hwnd)
            self.client_width = client_rect[2]
            self.client_height = client_rect[3]
            
            print(f"📐 窗口大小: {self.width}x{self.height}, 客户区: {self. client_width}x{self. client_height}")
        except Exception as e:
            print(f"⚠️ 更新窗口大小失败: {e}")
            self.width = 800
            self.height = 600
            self.client_width = 800
            self.client_height = 600
    
    def capture_with_printwindow(self):
        """
        方法1: 使用 PrintWindow API（最适合 DirectX 游戏）
        """
        print("🎮 尝试 PrintWindow 方法...")
        
        # 先尝试激活窗口
        try:
            if win32gui.IsIconic(self.hwnd):
                win32gui.ShowWindow(self.hwnd, 9)  # SW_RESTORE
            time.sleep(0.1)
        except: 
            pass
        
        # 获取窗口DC
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        
        # 使用客户区大小
        width = self.client_width if self.client_width > 0 else self.width
        height = self. client_height if self.client_height > 0 else self. height
        
        # 创建位图
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        
        # 使用 PrintWindow（关键！）
        # 参数3:  0=默认, 1=PW_CLIENTONLY, 2=PW_RENDERFULLCONTENT, 3=两者结合
        result = windll.user32.PrintWindow(self.hwnd, saveDC. GetSafeHdc(), 3)
        
        if result == 0:
            print("⚠️ PrintWindow 返回失败")
        
        # 给游戏一点时间渲染
        time.sleep(0.05)
        
        # 转换为 PIL Image
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )
        
        # 清理
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        
        return img
    
    def capture_with_bitblt(self):
        """
        方法2: 使用 BitBlt（传统方法）
        """
        print("📸 尝试 BitBlt 方法...")
        
        hwndDC = win32gui. GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        
        width = self.client_width if self.client_width > 0 else self.width
        height = self.client_height if self. client_height > 0 else self.height
        
        saveBitMap = win32ui. CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        
        result = saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
        
        bmpinfo = saveBitMap. GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )
        
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC. DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        
        return img
    
    def capture_screen_region(self):
        """
        方法3: 截取屏幕上窗口所在区域（最后的手段）
        """
        print("🖥️ 尝试屏幕区域截取...")
        
        from PIL import ImageGrab
        
        # 获取窗口在屏幕上的位置
        rect = win32gui. GetWindowRect(self.hwnd)
        
        # 截取屏幕区域
        img = ImageGrab.grab(bbox=rect)
        
        return img
    
    def _is_all_black(self, img):
        """检查图片是否全黑"""
        arr = np.array(img)
        avg_brightness = arr.mean()
        max_brightness = arr.max()
        
        print(f"  图片亮度 - 平均: {avg_brightness:.1f}, 最大: {max_brightness}")
        
        return max_brightness < 10
    
    def capture(self, method='auto'):
        """
        智能截图 - 自动尝试多种方法
        : param method: 'auto', 'printwindow', 'bitblt', 'screen'
        """
        self.update_window_size()
        
        if method == 'auto':
            # 方法1: PrintWindow (最适合游戏)
            try:
                img = self.capture_with_printwindow()
                if not self._is_all_black(img):
                    print("✅ PrintWindow 成功！")
                    return img
                else:
                    print("⚠️ PrintWindow 截图全黑")
            except Exception as e:
                print(f"❌ PrintWindow 失败: {e}")
            
            # 方法2: BitBlt
            try:
                img = self.capture_with_bitblt()
                if not self._is_all_black(img):
                    print("✅ BitBlt 成功！")
                    return img
                else: 
                    print("⚠️ BitBlt 截图全黑")
            except Exception as e:
                print(f"❌ BitBlt 失败: {e}")
            
            # 方法3: 屏幕截取（需要窗口可见）
            try:
                print("⚠️ 前两种方法都失败，尝试屏幕截取（需要游戏窗口可见）")
                img = self.capture_screen_region()
                if not self._is_all_black(img):
                    print("✅ 屏幕截取成功！")
                    return img
            except Exception as e:
                print(f"❌ 屏幕截取失败:  {e}")
            
            raise Exception("所有截图方法都失败了！")
        
        elif method == 'printwindow': 
            return self.capture_with_printwindow()
        elif method == 'bitblt':
            return self.capture_with_bitblt()
        elif method == 'screen':
            return self. capture_screen_region()
    
    def save_screenshot(self, filename):
        """保存截图"""
        try:
            img = self.capture()
            img.save(filename, 'PNG')
            
            import os
            size = os.path.getsize(filename)
            print(f"✅ 截图已保存: {filename} ({img.width}x{img.height}, {size/1024:.1f}KB)")
            
            return filename
        except Exception as e: 
            print(f"❌ 保存截图失败:  {e}")
            raise
    
    def capture_to_numpy(self):
        """截取并转换为 numpy 数组（用于 OpenCV）"""
        img = self.capture()
        # PIL 是 RGB，OpenCV 是 BGR
        return np.array(img)[: , :, ::-1]. copy()
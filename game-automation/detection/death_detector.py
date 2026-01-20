"""
死亡检测器 - 检测怪物是否死亡
"""
import cv2
import numpy as np
from typing import Tuple
import time

class DeathDetector:  
    """怪物死亡检测器"""
    
    def __init__(self):
        # 红色血条的HSV范围
        self.hp_bar_lower = np.array([0, 100, 100])
        self.hp_bar_upper = np.array([10, 255, 255])
        self.hp_bar_lower2 = np.array([170, 100, 100])
        self.hp_bar_upper2 = np.array([180, 255, 255])
    
    def is_monster_alive(self, image, monster_region):
        """
        检测怪物是否还活着 - 通过血条
        """
        x, y, w, h = monster_region
        
        # 在怪物上方区域查找血条
        search_y = max(0, y - 20)
        search_height = 25
        search_x = max(0, x)
        search_width = w
        
        roi = image[search_y:search_y + search_height, 
                   search_x:search_x + search_width]
        
        if roi.size == 0:
            return False
        
        # 转换到HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # 检测红色
        mask1 = cv2.inRange(hsv, self.hp_bar_lower, self.hp_bar_upper)
        mask2 = cv2.inRange(hsv, self.hp_bar_lower2, self.hp_bar_upper2)
        mask = cv2.bitwise_or(mask1, mask2)
        
        # 如果有足够的红色像素，说明血条还在
        red_pixels = cv2.countNonZero(mask)
        
        return red_pixels > 5  # 至少5个红色像素
    
    def wait_for_death(self, capture_func, monster_region, max_wait=10.0, check_interval=0.5):
        """
        等待怪物死亡
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            img = capture_func()
            
            if not self.is_monster_alive(img, monster_region):
                return True
            
            time.sleep(check_interval)
        
        return False
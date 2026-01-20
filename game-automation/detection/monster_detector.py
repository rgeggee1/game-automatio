"""
怪物检测器 - 优化点击位置
"""
import cv2
import numpy as np
from typing import List, Tuple, Optional

class MonsterDetector:
    """怪物检测器 - 专为细血条优化"""
    
    def __init__(self):
        # 血条颜色
        self.hp_bar_lower = np.array([0, 100, 100])
        self.hp_bar_upper = np.array([10, 255, 255])
        self.hp_bar_lower2 = np.array([170, 100, 100])
        self.hp_bar_upper2 = np.array([180, 255, 255])
        
        # 检测区域
        self.detect_region = {
            'x': 100,
            'y': 100,
            'width': 800,
            'height': 450
        }
        
        # 血条特征 30x2
        self.hp_bar_min_width = 15
        self.hp_bar_max_width = 50
        self.hp_bar_min_height = 1
        self.hp_bar_max_height = 5
        self.hp_bar_min_ratio = 5.0
    
    def detect_monsters_by_hp_bar(self, image):
        """
        检测怪物 - 返回怪物信息字典列表
        """
        region = self.detect_region
        roi = image[region['y']:region['y']+region['height'], 
                   region['x']:region['x']+region['width']]
        
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        mask1 = cv2.inRange(hsv, self.hp_bar_lower, self.hp_bar_upper)
        mask2 = cv2.inRange(hsv, self.hp_bar_lower2, self.hp_bar_upper2)
        mask = cv2.bitwise_or(mask1, mask2)
        
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        monsters = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            if not self._is_hp_bar(w, h):
                continue
            
            # 转换回原图坐标
            abs_x = region['x'] + x
            abs_y = region['y'] + y
            
            # 点击位置 = 血条中心下方35像素
            click_x = abs_x + w // 2
            click_y = abs_y + 50
            
            # 返回字典格式
            monsters.append({
                'click_pos': (click_x, click_y),
                'hp_bar':  (abs_x, abs_y, w, h),
                'center': (click_x, click_y)
            })
        
        return monsters
    
    def _is_hp_bar(self, w, h):
        """判断是否是血条"""
        if not (self.hp_bar_min_width <= w <= self.hp_bar_max_width):
            return False
        if not (self.hp_bar_min_height <= h <= self. hp_bar_max_height):
            return False
        if h == 0:
            return False
        ratio = w / h
        if ratio < self.hp_bar_min_ratio:
            return False
        return True
    
    def find_nearest_monster(self, monsters, player_pos=(512, 384)):
        """
        找最近的怪物
        返回:  怪物字典 {'click_pos': (x, y), 'hp_bar': (x, y, w, h), 'center': (x, y)}
        """
        if not monsters:
            return None
        
        def distance(monster):
            cx, cy = monster['click_pos']
            dx = cx - player_pos[0]
            dy = cy - player_pos[1]
            return (dx * dx + dy * dy) ** 0.5
        
        return min(monsters, key=distance)
    
    def visualize_detection(self, image, monsters):
        """可视化检测结果"""
        result = image.copy()
        
        region = self.detect_region
        cv2.rectangle(result, 
                     (region['x'], region['y']), 
                     (region['x'] + region['width'], region['y'] + region['height']),
                     (255, 255, 0), 2)
        
        cv2.putText(result, "Detection Region", 
                   (region['x'] + 5, region['y'] + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        for i, monster in enumerate(monsters):
            hp_x, hp_y, hp_w, hp_h = monster['hp_bar']
            click_x, click_y = monster['click_pos']
            
            # 血条 - 红色
            cv2.rectangle(result, (hp_x, hp_y), (hp_x + hp_w, hp_y + hp_h), (0, 0, 255), 2)
            
            # 点击位置 - 绿色圆圈
            cv2.circle(result, (click_x, click_y), 8, (0, 255, 0), 2)
            cv2.circle(result, (click_x, click_y), 2, (0, 255, 0), -1)
            
            # 标签
            cv2.putText(result, f"M{i+1}", (click_x - 10, click_y - 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return result
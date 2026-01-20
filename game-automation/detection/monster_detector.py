"""
怪物检测模块 - 使用颜色检测识别游戏中的怪物
"""
import cv2
import numpy as np
from typing import List, Tuple, Optional


class MonsterDetector:
    """怪物检测器 - 基于颜色特征检测游戏中的怪物"""
    
    def __init__(self, config=None):
        """
        初始化怪物检测器
        :param config: 配置字典，包含颜色范围等参数
        """
        self.config = config or {}
        
        # 从配置加载参数，使用默认值作为后备
        monster_cfg = self.config.get('monster_detection', {})
        
        # 是否使用HSV色彩空间
        self.use_hsv = monster_cfg.get('use_hsv', True)
        
        # HSV颜色范围（红色） - 调整为更宽松的范围
        self.red_lower1 = np.array(monster_cfg.get('red_lower1', [0, 50, 50]))
        self.red_upper1 = np.array(monster_cfg.get('red_upper1', [10, 255, 255]))
        self.red_lower2 = np.array(monster_cfg.get('red_lower2', [160, 50, 50]))
        self.red_upper2 = np.array(monster_cfg.get('red_upper2', [180, 255, 255]))
        
        # BGR颜色范围（备选）
        self.monster_color_lower = np.array([0, 0, 150])    # BGR格式: 蓝色通道低
        self.monster_color_upper = np.array([100, 100, 255])  # BGR格式: 红色通道高
        
        # 检测阈值
        self.min_monster_area = monster_cfg.get('min_area', 50)   # 最小怪物面积（像素）
        self.max_monster_area = monster_cfg.get('max_area', 15000)  # 最大怪物面积（像素）
    
    def detect(self, image: np.ndarray, detection_region: Optional[Tuple[int, int, int, int]] = None) -> List[dict]:
        """
        检测图像中的怪物
        :param image: 输入图像 (BGR格式的numpy数组)
        :param detection_region: 检测区域 (x, y, width, height)，None表示全图
        :return: 检测到的怪物列表，每个怪物包含位置和大小信息
        """
        if image is None or image.size == 0:
            return []
        
        # 如果指定了检测区域，裁剪图像
        offset_x, offset_y = 0, 0
        if detection_region is not None:
            x, y, w, h = detection_region
            offset_x, offset_y = x, y
            # 确保区域在图像范围内
            x = max(0, min(x, image.shape[1]))
            y = max(0, min(y, image.shape[0]))
            w = min(w, image.shape[1] - x)
            h = min(h, image.shape[0] - y)
            image = image[y:y+h, x:x+w]
        
        # 颜色阈值检测
        if self.use_hsv:
            # 转换到HSV色彩空间
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # 红色在HSV中分布在两端，需要两个mask
            mask1 = cv2.inRange(hsv, self.red_lower1, self.red_upper1)
            mask2 = cv2.inRange(hsv, self.red_lower2, self.red_upper2)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            # BGR颜色空间检测
            mask = cv2.inRange(image, self.monster_color_lower, self.monster_color_upper)
        
        # 形态学操作 - 只使用膨胀来连接近邻像素，不使用开运算以避免删除小区域
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=3)  # 膨胀以连接近邻像素形成团块
        
        # 查找轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        monsters = []
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # 过滤太小或太大的区域
            if area < self.min_monster_area or area > self.max_monster_area:
                continue
            
            # 获取边界框
            x, y, w, h = cv2.boundingRect(contour)
            
            # 计算中心点（加上偏移量，转换回原图坐标）
            center_x = x + w // 2 + offset_x
            center_y = y + h // 2 + offset_y
            
            # 添加到怪物列表
            monsters.append({
                'center': (center_x, center_y),
                'bbox': (x + offset_x, y + offset_y, w, h),
                'area': area
            })
        
        return monsters
    
    def visualize(self, image: np.ndarray, monsters: List[dict], 
                  detection_region: Optional[Tuple[int, int, int, int]] = None,
                  output_path: str = 'monster_detection_result.png') -> str:
        """
        生成可视化结果图
        :param image: 原始图像 (BGR格式)
        :param monsters: 检测到的怪物列表
        :param detection_region: 检测区域
        :param output_path: 输出文件路径
        :return: 输出文件路径
        """
        # 复制图像用于绘制
        vis_image = image.copy()
        
        # 绘制检测区域
        if detection_region is not None:
            x, y, w, h = detection_region
            cv2.rectangle(vis_image, (x, y), (x + w, y + h), (255, 255, 0), 2)  # 青色边框
            # 在检测区域左上角添加文字
            cv2.putText(vis_image, 'Detection Region', (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # 绘制检测到的怪物
        for i, monster in enumerate(monsters):
            center = monster['center']
            bbox = monster['bbox']
            
            # 绘制边界框 (红色)
            x, y, w, h = bbox
            cv2.rectangle(vis_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
            # 绘制中心点 (绿色)
            cv2.circle(vis_image, center, 5, (0, 255, 0), -1)
            
            # 绘制编号
            label = f'#{i+1}'
            cv2.putText(vis_image, label, (center[0] - 10, center[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # 保存图像
        cv2.imwrite(output_path, vis_image)
        return output_path

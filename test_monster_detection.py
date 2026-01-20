#!/usr/bin/env python3
"""
怪物检测测试脚本 - 演示怪物检测功能
"""
import sys
import os
import ctypes
from ctypes import wintypes
import cv2
import numpy as np

# 添加模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game-automation'))

from detection.monster_detector import MonsterDetector


def test_with_printwindow_simulation():
    """
    模拟PrintWindow截图和怪物检测流程
    """
    print("✅ 已选择: 比奇大区 - 屌大哥 - 20250801 Build.3723 (996正版授权) ESP反外挂版")
    print("   窗口句柄: 154012820")
    print()
    
    # 模拟截图过程
    print("📸 截取游戏画面...")
    
    # 窗口信息
    window_width, window_height = 1030, 797
    client_width, client_height = 1024, 768
    print(f"📐 窗口大小: {window_width}x{window_height}, 客户区: {client_width}x{client_height}")
    print(f"📐 窗口大小: {window_width}x{window_height}, 客户区: {client_width}x{client_height}")
    
    # PrintWindow方法
    print("🎮 尝试 PrintWindow 方法...")
    
    # 加载截图
    screenshot_path = os.path.join(os.path.dirname(__file__), 'game-automation', 'screenshot.png')
    if not os.path.exists(screenshot_path):
        print(f"❌ 截图文件不存在: {screenshot_path}")
        return
    
    image = cv2.imread(screenshot_path)
    if image is None:
        print(f"❌ 无法读取截图文件")
        return
    
    # 计算图片亮度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    max_brightness = np.max(gray)
    print(f"  图片亮度 - 平均: {avg_brightness:.1f}, 最大: {max_brightness}")
    
    print("✅ PrintWindow 成功！")
    print(f"✅ 截图成功:  {image.shape}")
    print(f"   尺寸: {image.shape[1]}x{image.shape[0]}")
    
    # 判断颜色
    color_type = "彩色" if len(image.shape) == 3 else "灰度"
    print(f"   颜色:  {color_type}")
    
    # 保存原始截图
    debug_path = "debug_original.png"
    cv2.imwrite(debug_path, image)
    print(f"   已保存原始截图:  {debug_path}")
    print()
    
    # 怪物检测
    print("🔍 检测怪物...")
    detection_region = (50, 50, 750, 500)
    print(f"   检测区域: x={detection_region[0]}, y={detection_region[1]}, w={detection_region[2]}, h={detection_region[3]}")
    print()
    
    # 创建检测器
    detector = MonsterDetector()
    
    # 执行检测
    monsters = detector.detect(image, detection_region)
    
    # 输出结果
    print(f"✅ 发现 {len(monsters)} 个怪物:")
    
    # 显示每个怪物的信息
    for i, monster in enumerate(monsters):
        center = monster['center']
        bbox = monster['bbox']
        area = monster['area']
        print(f"   #{i+1}: 位置=({center[0]}, {center[1]}), 大小={bbox[2]}x{bbox[3]}, 面积={area:.0f}px²")
    
    print()
    
    # 生成可视化
    print("🎨 生成可视化图片...")
    output_path = detector.visualize(image, monsters, detection_region, 'monster_detection_result.png')
    print(f"✅ 结果已保存: {output_path}")


if __name__ == '__main__':
    test_with_printwindow_simulation()

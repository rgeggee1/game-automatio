# 怪物检测功能说明

## 功能概述

本模块实现了基于颜色检测的怪物识别功能，能够从游戏截图中自动识别红色系怪物。

## 主要特性

- ✅ 使用 HSV 色彩空间进行颜色检测，提高准确性
- ✅ 支持自定义检测区域
- ✅ 可配置的颜色阈值和面积过滤
- ✅ 生成可视化结果图
- ✅ 输出详细的检测信息

## 使用方法

### 1. 基本使用

```python
from detection.monster_detector import MonsterDetector
import cv2

# 加载图像
image = cv2.imread('screenshot.png')

# 创建检测器
detector = MonsterDetector()

# 执行检测（指定检测区域）
detection_region = (50, 50, 750, 500)  # (x, y, width, height)
monsters = detector.detect(image, detection_region)

# 输出结果
print(f"发现 {len(monsters)} 个怪物")
for i, monster in enumerate(monsters):
    center = monster['center']
    bbox = monster['bbox']
    print(f"#{i+1}: 位置=({center[0]}, {center[1]})")

# 生成可视化图
detector.visualize(image, monsters, detection_region, 'result.png')
```

### 2. 使用配置文件

```python
import yaml
from detection.monster_detector import MonsterDetector

# 加载配置
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 使用配置创建检测器
detector = MonsterDetector(config['detection'])

# 执行检测
monsters = detector.detect(image, detection_region)
```

### 3. 运行测试脚本

```bash
python3 test_monster_detection.py
```

## 配置说明

在 `config.yaml` 文件中可以配置以下参数：

```yaml
detection:
  monster_detection:
    use_hsv: true                    # 是否使用HSV色彩空间
    red_lower1: [0, 50, 50]          # 红色检测范围1 [H, S, V]
    red_upper1: [10, 255, 255]
    red_lower2: [160, 50, 50]        # 红色检测范围2
    red_upper2: [180, 255, 255]
    min_area: 50                     # 最小怪物面积（像素）
    max_area: 15000                  # 最大怪物面积（像素）
```

### 参数说明

- **use_hsv**: 是否使用 HSV 色彩空间（推荐开启）
- **red_lower1/red_upper1**: HSV 红色范围 1（0-10度）
- **red_lower2/red_upper2**: HSV 红色范围 2（160-180度）
- **min_area**: 过滤掉小于此面积的区域
- **max_area**: 过滤掉大于此面积的区域

## 输出格式

检测结果为字典列表，每个怪物包含：

```python
{
    'center': (x, y),           # 中心点坐标
    'bbox': (x, y, w, h),       # 边界框 (左上角x, y, 宽度, 高度)
    'area': float               # 面积（像素²）
}
```

## 可视化输出

生成的可视化图像包含：

- 🟦 青色边框：检测区域
- 🟥 红色边框：检测到的怪物
- 🟢 绿色圆点：怪物中心点
- 🔢 编号标签：怪物序号

## 示例输出

```
✅ 已选择: 比奇大区 - 屌大哥 - 20250801 Build.3723 (996正版授权) ESP反外挂版
   窗口句柄: 154012820

📸 截取游戏画面...
📐 窗口大小: 1030x797, 客户区: 1024x768
🎮 尝试 PrintWindow 方法...
  图片亮度 - 平均: 93.9, 最大: 255
✅ PrintWindow 成功！
✅ 截图成功:  (768, 1024, 3)
   尺寸: 1024x768
   颜色:  彩色

🔍 检测怪物...
   检测区域: x=50, y=50, w=750, h=500

✅ 发现 14 个怪物:
   #1: 位置=(663, 545), 大小=13x9, 面积=96px²
   #2: 位置=(574, 538), 大小=20x24, 面积=322px²
   ...

🎨 生成可视化图片...
✅ 结果已保存: monster_detection_result.png
```

## 技术细节

### 检测流程

1. **颜色空间转换**: BGR → HSV
2. **颜色阈值过滤**: 提取红色区域
3. **形态学处理**: 膨胀操作连接近邻像素
4. **轮廓检测**: 查找独立区域
5. **面积过滤**: 过滤异常大小的区域
6. **坐标转换**: 转换回原图坐标系

### HSV 色彩空间优势

- 对光照变化更鲁棒
- 更容易分离颜色信息
- 红色处理更准确（分布在 H 的两端）

## 注意事项

1. 确保游戏截图是 BGR 格式（OpenCV 默认）
2. 检测区域坐标是相对于原图的绝对坐标
3. 红色系检测适用于大多数游戏中的敌对单位
4. 可根据实际游戏调整颜色范围参数

## 依赖库

- OpenCV (cv2)
- NumPy
- PyYAML (用于配置加载)

## 许可证

本项目使用开源许可证。

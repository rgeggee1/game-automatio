"""
打怪策略 - 整合检测和动作
"""
import time
from detection.monster_detector import MonsterDetector
from actions.combat import CombatActions
from actions.looting import LootingActions

class HuntingStrategy:
    """打怪策略控制器"""
    
    def __init__(self, screen_capture, input_controller):
        self.screen_capture = screen_capture
        self.input_ctrl = input_controller
        
        # 初始化各模块
        self.monster_detector = MonsterDetector()
        self.combat = CombatActions(input_controller)
        self.looting = LootingActions(input_controller)
        
        # 配int, int, int, int]):
        """
        拾取尸体
        :param corpse_pos: 尸体位置 (x, y, w, h)
        """
        x, y, w, h = corpse_pos
        center_x = x + w // 2
        center_y = y + h // 2
        
        print(f"  💰 点击尸体: ({center_x}, {center_y})")
        self.input.click_input(center_x, center_y, restore_cursor=True)
        time.sleep(0.3)
        
        print(f"  💰 按F键拾取...")
        self.input.send_key(self.loot_key)
        time.sleep(0.5)
    
    def auto_loot_nearby(self, positions: list):
        """
        自动拾取多个位置的物品
        """
        for pos in positions:
            self. loot_corpse(pos)
            time.sleep(0.2)
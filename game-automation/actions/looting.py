"""
拾取动作 - 拾取物品
"""
import time
from typing import Tuple

class LootingActions:
    """拾取动作控制器"""
    
    def __init__(self, input_controller):
        self.input = input_controller
        self.loot_key = 0x46  # F键
    
    def loot_corpse(self, corpse_pos):
        """
        拾取尸体
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
    
    def auto_loot_nearby(self, positions):
        """
        自动拾取多个位置的物品
        """
        for pos in positions:
            self. loot_corpse(pos)
            time.sleep(0.2)
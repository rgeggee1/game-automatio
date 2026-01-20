"""
战斗动作 - 攻击、释放技能
"""
import time
from typing import Tuple, Optional

class CombatActions:
    """战斗动作控制器"""
    
    def __init__(self, input_controller):
        self.input = input_controller
        
        # 技能配置
        self.skills = [0x70, 0x71, 0x72, 0x73]  # F1, F2, F3, F4
        self.current_skill_index = 0
        
        # 时间配置
        self.attack_interval = 0.8  # 攻击间隔
        self.skill_cooldown = 0.3   # 技能间隔
    
    def click_monster(self, monster_pos):
        """
        点击怪物 - 选中目标
        """
        x, y, w, h = monster_pos
        center_x = x + w // 2
        center_y = y + h // 2
        
        print(f"  👆 点击怪物:  ({center_x}, {center_y})")
        self.input.click_input(center_x, center_y, restore_cursor=True)
        time.sleep(0.2)
    
    def use_skill(self, skill_index=None):
        """
        释放技能
        """
        if skill_index is None:
            skill_index = self.current_skill_index
            self.current_skill_index = (self.current_skill_index + 1) % len(self.skills)
        
        skill_vk = self.skills[skill_index]
        skill_name = f"F{skill_index + 1}"
        
        print(f"  ⚡ 释放技能: {skill_name}")
        self.input.send_key(skill_vk)
        time.sleep(self.skill_cooldown)
    
    def attack_monster(self, monster_pos):
        """
        攻击怪物 - 点击 + 释放技能
        """
        self.click_monster(monster_pos)
        self.use_skill()
    
    def continuous_attack(self, monster_pos, duration=3.0):
        """
        持续攻击
        """
        start_time = time.time()
        
        while time.time() - start_time < duration: 
            self.attack_monster(monster_pos)
            time.sleep(self.attack_interval)
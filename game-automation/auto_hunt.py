"""
自动打怪主程序 - 智能等待版
"""
import time
from core.window_manager import WindowManager
from core.screen_capture_advanced import ScreenCaptureAdvanced
from core.input_controller import InputController
from detection.monster_detector import MonsterDetector
from actions.looting import LootingActions

def main():
    print("=" * 60)
    print("🎮 自动打怪程序 v2.2 - 智能等待版")
    print("=" * 60)
    
    # 选择窗口
    print("\n📋 可用窗口:")
    wm = WindowManager()
    windows = wm.get_all_windows()
    
    for i, w in enumerate(windows[: 10]):
        print(f"  [{i}] {w.title}")
    
    choice = int(input("\n请选择游戏窗口编号:  "))
    hwnd = windows[choice]. hwnd
    
    print(f"\n✅ 已选择:  {windows[choice].title}")
    
    # 初始化
    print("\n⚙️ 初始化模块...")
    capturer = ScreenCaptureAdvanced(hwnd)
    input_ctrl = InputController(hwnd)
    monster_detector = MonsterDetector()
    loot = LootingActions(input_ctrl)
    
    print("✅ 所有模块已就绪")
    
    # 配置
    print("\n⚙️ 配置:")
    max_attack_time = float(input("最大攻击等待时间(秒) [默认15]: ") or "15")
    check_interval = float(input("检测血条间隔(秒) [默认1. 5]: ") or "1.5")
    loot_wait = float(input("击杀后拾取延迟(秒) [默认2]:  ") or "2")
    
    print("\n" + "=" * 60)
    print("🚀 ��始自动打怪！")
    print("💡 按 Ctrl+C 停止")
    print("=" * 60 + "\n")
    
    killed_count = 0
    
    try:
        while True:
            # 1. 截图检测怪物
            img = capturer.capture_to_numpy()
            monsters = monster_detector.detect_monsters_by_hp_bar(img)
            
            if not monsters:
                print("⏳ 没有发现怪物，等待中...")
                time.sleep(2)
                continue
            
            # 2. 选择最近的怪物
            monster = monster_detector.find_nearest_monster(monsters)
            
            click_x, click_y = monster['click_pos']
            hp_x, hp_y, hp_w, hp_h = monster['hp_bar']
            
            print(f"\n🎯 发现怪物: 点击位置=({click_x}, {click_y}), 共{len(monsters)}个怪物")
            print(f"   血条位置: ({hp_x}, {hp_y}), 大小={hp_w}×{hp_h}")
            
            # 3. 点击怪物
            print(f"👆 点击怪物...")
            input_ctrl.click_input(click_x, click_y, restore_cursor=True)
            
            # 4. 智能等待：持续检测血条直到消失
            print(f"⚔️ 等待角色攻击（最长{max_attack_time}秒，每{check_interval}秒检测一次）...")
            
            start_time = time.time()
            hp_disappeared = False
            check_count = 0
            
            while time.time() - start_time < max_attack_time: 
                time.sleep(check_interval)
                check_count += 1
                
                # 检测血条是否还在
                img_check = capturer.capture_to_numpy()
                monsters_check = monster_detector.detect_monsters_by_hp_bar(img_check)
                
                # 检查同一位置的血条是否还在
                hp_still_exists = False
                for m in monsters_check:
                    check_hp_x, check_hp_y, _, _ = m['hp_bar']
                    if abs(check_hp_x - hp_x) < 20 and abs(check_hp_y - hp_y) < 20:
                        hp_still_exists = True
                        break
                
                if not hp_still_exists:
                    elapsed = time.time() - start_time
                    print(f"   ✅ 血条消失！耗时 {elapsed:.1f}秒（检测{check_count}次）")
                    hp_disappeared = True
                    break
                else:
                    print(f"   ⏳ 第{check_count}次检测：血条还在，继续等待...")
            
            # 5. 判断结果
            if hp_disappeared: 
                print("💀 怪物已死亡！")
                killed_count += 1
                
                # 6. 拾取
                print(f"💰 等待{loot_wait}秒后拾取...")
                time.sleep(loot_wait)
                
                print(f"💰 拾取尸体...")
                input_ctrl.click_input(click_x, click_y, restore_cursor=True)
                time.sleep(0.3)
                input_ctrl.send_key(0x46)  # F键
                
                print(f"\n✅ 已击杀: {killed_count} 个怪物\n")
                time.sleep(1)
            else:
                print(f"⚠️ 超时{max_attack_time}秒，怪物可能还活着或已逃跑")
                print("   跳过此怪物，寻找下一个目标...")
                time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("⏹️ 停止自动打怪")
        print(f"📊 总击杀:  {killed_count} 个怪物")
        print("=" * 60)

if __name__ == '__main__':
    main()
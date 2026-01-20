"""
测试面板 - 精简版（移除调试按钮，添加增强截图）
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QPushButton, QLabel, QSpinBox, QCheckBox)
from PyQt6.QtCore import Qt
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.input_controller import InputController

class TestPanel(QWidget):
    """输入控制测试面板"""
    
    def __init__(self, window_manager, parent=None):
        super().__init__(parent)
        self.window_manager = window_manager
        self.input_controller = None
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # ========== 鼠标测试组 ==========
        mouse_group = QGroupBox("🖱️ 鼠标控制测试")
        mouse_layout = QVBoxLayout()
        
        # 后台选项
        background_layout = QHBoxLayout()
        self.checkbox_restore_cursor = QCheckBox("🎯 点击后恢复光标位置（伪后台模式）")
        self.checkbox_restore_cursor.setChecked(True)
        self.checkbox_restore_cursor.setStyleSheet("color: #0066cc; font-weight: bold;")
        background_layout.addWidget(self.checkbox_restore_cursor)
        background_layout.addStretch()
        mouse_layout.addLayout(background_layout)
        
        # 坐标输入
        coord_layout = QHBoxLayout()
        coord_layout.addWidget(QLabel("X坐标:"))
        self.mouse_x = QSpinBox()
        self.mouse_x.setRange(0, 3000)
        self.mouse_x.setValue(500)
        coord_layout.addWidget(self. mouse_x)
        
        coord_layout.addWidget(QLabel("Y坐标: "))
        self.mouse_y = QSpinBox()
        self.mouse_y.setRange(0, 3000)
        self.mouse_y.setValue(500)
        coord_layout.addWidget(self.mouse_y)
        
        btn_get_pos = QPushButton("📍 获取当前鼠标位置")
        btn_get_pos.clicked. connect(self.get_current_mouse_pos)
        coord_layout.addWidget(btn_get_pos)
        
        mouse_layout.addLayout(coord_layout)
        
        # 鼠标按钮
        mouse_btn_layout = QHBoxLayout()
        
        btn_move = QPushButton("移动鼠标")
        btn_move.clicked.connect(self. test_mouse_move)
        mouse_btn_layout.addWidget(btn_move)
        
        btn_left_click = QPushButton("左键点击")
        btn_left_click.clicked.connect(self.test_left_click)
        btn_left_click.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        mouse_btn_layout.addWidget(btn_left_click)
        
        btn_right_click = QPushButton("右键点击")
        btn_right_click.clicked.connect(self. test_right_click)
        btn_right_click.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        mouse_btn_layout.addWidget(btn_right_click)
        
        mouse_layout.addLayout(mouse_btn_layout)
        
        coord_hint = QLabel("💡 提示：坐标为客户区坐标，(0,0) 是游戏窗口左上角")
        coord_hint.setStyleSheet("color: #666; font-size: 10px; padding: 5px;")
        mouse_layout.addWidget(coord_hint)
        
        mouse_group.setLayout(mouse_layout)
        layout.addWidget(mouse_group)
        
        # ========== 键盘测试组 ==========
        keyboard_group = QGroupBox("⌨️ 键盘控制测试")
        keyboard_layout = QVBoxLayout()
        
        # 功能按键 F1-F4
        func_label = QLabel("⚡ 技能按键 (F1-F4):")
        func_label.setStyleSheet("font-weight: bold; padding-top: 10px;")
        keyboard_layout.addWidget(func_label)
        
        func_key_layout = QHBoxLayout()
        func_keys = [
            ("F1", 0x70), ("F2", 0x71), ("F3", 0x72), ("F4", 0x73)
        ]
        
        for key_name, vk_code in func_keys:
            btn = QPushButton(key_name)
            btn.setMinimumWidth(80)
            btn.setMinimumHeight(40)
            btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px;")
            btn.clicked.connect(lambda checked, vk=vk_code, name=key_name: self.send_key(vk, name))
            func_key_layout. addWidget(btn)
        
        func_key_layout.addStretch()
        keyboard_layout.addLayout(func_key_layout)
        
        # 数字按键 1-6
        num_label = QLabel("🔢 物品/快捷键 (1-6):")
        num_label.setStyleSheet("font-weight:  bold; padding-top: 10px;")
        keyboard_layout.addWidget(num_label)
        
        num_key_layout = QHBoxLayout()
        num_keys = [
            ("1", 0x31), ("2", 0x32), ("3", 0x33),
            ("4", 0x34), ("5", 0x35), ("6", 0x36)
        ]
        
        for key_name, vk_code in num_keys: 
            btn = QPushButton(key_name)
            btn.setMinimumWidth(70)
            btn.setMinimumHeight(40)
            btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; font-size: 14px;")
            btn.clicked. connect(lambda checked, vk=vk_code, name=key_name: self.send_key(vk, name))
            num_key_layout.addWidget(btn)
        
        num_key_layout.addStretch()
        keyboard_layout.addLayout(num_key_layout)
        
        # 字母按键 M 和 F
        other_label = QLabel("🔧 其他按键:")
        other_label.setStyleSheet("font-weight: bold; padding-top: 10px;")
        keyboard_layout.addWidget(other_label)
        
        other_key_layout = QHBoxLayout()
        
        btn_m = QPushButton("M")
        btn_m.setMinimumWidth(80)
        btn_m.setMinimumHeight(40)
        btn_m.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; font-size: 14px;")
        btn_m.clicked. connect(lambda:  self.send_key(0x4D, "M"))
        other_key_layout.addWidget(btn_m)
        
        btn_f = QPushButton("F (拾取)")
        btn_f.setMinimumWidth(80)
        btn_f.setMinimumHeight(40)
        btn_f.setStyleSheet("background-color: #FF5722; color: white; font-weight: bold; font-size:  14px;")
        btn_f.clicked.connect(lambda: self.send_key(0x46, "F"))
        other_key_layout.addWidget(btn_f)
        
        other_key_layout.addStretch()
        keyboard_layout.addLayout(other_key_layout)
        
        key_hint = QLabel("💡 提示：F1-F4 使用 SendMessageW 到子窗口，数字键使用 PostMessageW 到子窗口")
        key_hint.setStyleSheet("color: #0066cc; font-size: 10px; padding: 5px; font-weight: bold;")
        keyboard_layout.addWidget(key_hint)
        
        keyboard_group.setLayout(keyboard_layout)
        layout.addWidget(keyboard_group)
        
        # ========== 截图测试组 ==========
        screenshot_group = QGroupBox("📸 截图测试")
        screenshot_layout = QVBoxLayout()
        
        btn_screenshot = QPushButton("📷 截取游戏画面 (DirectX兼容)")
        btn_screenshot.clicked.connect(self.test_screenshot)
        btn_screenshot.setStyleSheet("background-color: #673AB7; color: white; font-weight: bold; padding: 10px;")
        screenshot_layout.addWidget(btn_screenshot)
        
        self.screenshot_label = QLabel("截图将保存到：screenshot.png")
        self.screenshot_label.setStyleSheet("padding: 5px; color: #666;")
        screenshot_layout.addWidget(self.screenshot_label)
        
        screenshot_hint = QLabel("💡 自动尝试 PrintWindow、BitBlt、屏幕截取三种方法")
        screenshot_hint.setStyleSheet("color: #666; font-size: 10px; padding: 5px;")
        screenshot_layout.addWidget(screenshot_hint)
        
        screenshot_group.setLayout(screenshot_layout)
        layout.addWidget(screenshot_group)
        
        # 状态提示
        self.test_status = QLabel("请先选择游戏窗口后再进行测试")
        self.test_status.setStyleSheet("color: red; padding: 10px; font-weight: bold;")
        layout.addWidget(self.test_status)
        
        layout.addStretch()
    
    def update_controller(self, hwnd):
        """更新输入控制器"""
        if hwnd: 
            self.input_controller = InputController(hwnd)
            self.test_status.setText("✅ 输入控制器已就绪，可以开始测试")
            self.test_status.setStyleSheet("color: green; padding: 10px; font-weight: bold;")
        else:
            self.input_controller = None
            self.test_status.setText("请先选择游戏窗口后再进行测试")
            self.test_status.setStyleSheet("color: red; padding:  10px; font-weight:  bold;")
    
    def get_current_mouse_pos(self):
        """获取当前鼠标位置（客户区坐标）"""
        import win32api
        import win32gui
        
        pos = win32api.GetCursorPos()
        
        if self.window_manager. current_hwnd:
            # 转换为客户区坐标
            client_pos = win32gui. ScreenToClient(self.window_manager.current_hwnd, pos)
            self.mouse_x. setValue(client_pos[0])
            self.mouse_y. setValue(client_pos[1])
            self.test_status.setText(f"📍 客户区坐标:  ({client_pos[0]}, {client_pos[1]})")
        else:
            self.test_status.setText("❌ 请先选择游戏窗口")
        
        self.test_status.setStyleSheet("color: blue; padding: 10px; font-weight: bold;")
    
    def test_mouse_move(self):
        """测试鼠标移动"""
        if not self.input_controller:
            self.show_error("请先选择游戏窗口！")
            return
        
        x = self.mouse_x.value()
        y = self.mouse_y.value()
        
        # 客户区坐标，需要转换为屏幕坐标
        import win32gui
        screen_pos = win32gui.ClientToScreen(self.window_manager.current_hwnd, (x, y))
        self.input_controller.move_mouse(screen_pos[0], screen_pos[1])
        self.test_status.setText(f"✅ 已移动鼠标到客户区坐标 ({x}, {y})")
        self.test_status.setStyleSheet("color: blue; padding: 10px; font-weight: bold;")
    
    def test_left_click(self):
        """测试左键点击"""
        if not self.input_controller:
            self.show_error("请先选择游戏窗口！")
            return
        
        x = self.mouse_x.value()
        y = self.mouse_y.value()
        restore_cursor = self.checkbox_restore_cursor.isChecked()
        
        # 使用客户区坐标点击
        self.input_controller.click_input(x, y, 'left', restore_cursor=restore_cursor)
        
        status_text = f"✅ 已在客户区坐标 ({x}, {y}) 左键点击"
        if restore_cursor:
            status_text += " 🎯 (后台模式)"
        
        self.test_status.setText(status_text)
        self.test_status.setStyleSheet("color: blue; padding: 10px; font-weight: bold;")
    
    def test_right_click(self):
        """测试右键点击"""
        if not self.input_controller:
            self.show_error("请先选择游戏窗口！")
            return
        
        x = self.mouse_x.value()
        y = self.mouse_y.value()
        restore_cursor = self.checkbox_restore_cursor.isChecked()
        
        # 使用客户区坐标点击
        self.input_controller.click_input(x, y, 'right', restore_cursor=restore_cursor)
        
        status_text = f"✅ 已在客户区坐标 ({x}, {y}) 右键点击"
        if restore_cursor:
            status_text += " 🎯 (后台模式)"
        
        self.test_status. setText(status_text)
        self.test_status.setStyleSheet("color: blue; padding:  10px; font-weight:  bold;")
    
    def send_key(self, vk_code, key_name):
        """发送按键"""
        if not self.input_controller:
            self.show_error("请先选择游戏窗口！")
            return
        
        # 使用窗口消息直投方式
        self.input_controller.send_key(vk_code)
        
        self.test_status.setText(f"✅ 已发送按键:  {key_name} (VK:  0x{vk_code: 02X})")
        self.test_status.setStyleSheet("color: blue; padding: 10px; font-weight: bold;")
    
    def test_screenshot(self):
        """测试截图（增强版 - 支持DirectX游戏）"""
        if not self.window_manager.current_hwnd:
            self.show_error("请先选择游戏窗口！")
            return
        
        try:
            self.test_status.setText("📸 正在截图（DirectX兼容模式）...")
            self.test_status.setStyleSheet("color: orange; padding: 10px; font-weight: bold;")
            
            # 使用增强版截图
            from core.screen_capture_advanced import ScreenCaptureAdvanced
            
            capturer = ScreenCaptureAdvanced(self.window_manager. current_hwnd)
            filename = "screenshot.png"
            
            print("\n" + "="*60)
            print("🎮 开始截取游戏画面...")
            print("="*60)
            
            result = capturer.save_screenshot(filename)
            
            import os
            if os.path. exists(filename):
                file_size = os.path.getsize(filename)
                self. screenshot_label.setText(f"✅ 截图已保存: {filename} ({file_size/1024:.1f} KB)")
                self.screenshot_label.setStyleSheet("padding: 5px; color: green; font-weight: bold;")
                
                self.test_status.setText(f"✅ 截图成功！请查看 {filename}")
                self.test_status.setStyleSheet("color: green; padding:  10px; font-weight:  bold;")
            else:
                self.show_error("截图文件未生成！")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.show_error(f"截图失败：{str(e)}")
    
    def show_error(self, message):
        """显示错误消息"""
        self.test_status.setText(f"❌ {message}")
        self.test_status.setStyleSheet("color: red; padding: 10px; font-weight: bold;")
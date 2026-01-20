"""
测试面板 - 用于测试输入控制功能
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QPushButton, QLabel, QLineEdit, QSpinBox)
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
        
        # 坐标输入
        coord_layout = QHBoxLayout()
        coord_layout.addWidget(QLabel("X坐标:"))
        self.mouse_x = QSpinBox()
        self.mouse_x.setRange(0, 2000)
        self.mouse_x.setValue(100)
        coord_layout.addWidget(self. mouse_x)
        
        coord_layout.addWidget(QLabel("Y坐标: "))
        self.mouse_y = QSpinBox()
        self.mouse_y.setRange(0, 2000)
        self.mouse_y.setValue(100)
        coord_layout.addWidget(self.mouse_y)
        mouse_layout.addLayout(coord_layout)
        
        # 鼠标按钮
        mouse_btn_layout = QHBoxLayout()
        
        btn_move = QPushButton("移动鼠标")
        btn_move.clicked.connect(self. test_mouse_move)
        mouse_btn_layout.addWidget(btn_move)
        
        btn_left_click = QPushButton("左键点击")
        btn_left_click.clicked.connect(self. test_left_click)
        mouse_btn_layout.addWidget(btn_left_click)
        
        btn_right_click = QPushButton("右键点击")
        btn_right_click.clicked.connect(self.test_right_click)
        mouse_btn_layout.addWidget(btn_right_click)
        
        mouse_layout.addLayout(mouse_btn_layout)
        mouse_group.setLayout(mouse_layout)
        layout.addWidget(mouse_group)
        
        # ========== 键盘测试组 ==========
        keyboard_group = QGroupBox("⌨️ 键盘控制测试")
        keyboard_layout = QVBoxLayout()
        
        # 虚拟键码输入
        vk_layout = QHBoxLayout()
        vk_layout.addWidget(QLabel("虚拟键码 (VK):"))
        self.vk_input = QLineEdit()
        self.vk_input.setPlaceholderText("例如:  0x57 (W键)")
        vk_layout.addWidget(self.vk_input)
        
        btn_send_key = QPushButton("发送按键")
        btn_send_key.clicked.connect(self. test_send_key)
        vk_layout.addWidget(btn_send_key)
        keyboard_layout.addLayout(vk_layout)
        
        # 常用按键快捷测试
        quick_key_layout = QHBoxLayout()
        
        keys = [
            ("W", 0x57), ("A", 0x41), ("S", 0x53), ("D", 0x44),
            ("空格", 0x20), ("1", 0x31), ("2", 0x32), ("F", 0x46)
        ]
        
        for key_name, vk_code in keys:
            btn = QPushButton(key_name)
            btn.clicked.connect(lambda checked, vk=vk_code: self.send_key(vk))
            quick_key_layout.addWidget(btn)
        
        keyboard_layout.addLayout(quick_key_layout)
        keyboard_group.setLayout(keyboard_layout)
        layout.addWidget(keyboard_group)
        
        # ========== 截图测试组 ==========
        screenshot_group = QGroupBox("📸 截图测试")
        screenshot_layout = QVBoxLayout()
        
        btn_screenshot = QPushButton("📷 截取游戏画面")
        btn_screenshot.clicked.connect(self.test_screenshot)
        screenshot_layout.addWidget(btn_screenshot)
        
        self.screenshot_label = QLabel("截图将保存到：screenshot.png")
        self.screenshot_label.setStyleSheet("padding: 5px; color: #666;")
        screenshot_layout.addWidget(self.screenshot_label)
        
        screenshot_group.setLayout(screenshot_layout)
        layout.addWidget(screenshot_group)
        
        # 状态提示
        self.test_status = QLabel("请先选择游戏窗口后再进行测试")
        self.test_status.setStyleSheet("color: red; padding: 10px; font-weight: bold;")
        layout.addWidget(self. test_status)
        
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
    
    def test_mouse_move(self):
        """测试鼠标移动"""
        if not self.input_controller:
            self.show_error("请先选择游戏窗口！")
            return
        
        x = self.mouse_x.value()
        y = self.mouse_y.value()
        
        self.input_controller.move_mouse(x, y)
        self.test_status.setText(f"✅ 已移动鼠标到 ({x}, {y})")
        self.test_status.setStyleSheet("color: blue; padding: 10px; font-weight: bold;")
    
    def test_left_click(self):
        """测试左键点击"""
        if not self.input_controller:
            self.show_error("请先选择游戏窗口！")
            return
        
        x = self.mouse_x.value()
        y = self.mouse_y.value()
        
        self.input_controller.click(x, y, 'left')
        self.test_status.setText(f"✅ 已在 ({x}, {y}) 左键点击")
        self.test_status.setStyleSheet("color: blue; padding: 10px; font-weight: bold;")
    
    def test_right_click(self):
        """测试右键点击"""
        if not self.input_controller:
            self.show_error("请先选择游戏窗口！")
            return
        
        x = self.mouse_x.value()
        y = self.mouse_y.value()
        
        self.input_controller.click(x, y, 'right')
        self.test_status.setText(f"✅ 已在 ({x}, {y}) 右键点击")
        self.test_status.setStyleSheet("color: blue; padding: 10px; font-weight: bold;")
    
    def send_key(self, vk_code):
        """发送按键"""
        if not self.input_controller:
            self.show_error("请先选择游戏窗口！")
            return
        
        self.input_controller.send_key(vk_code)
        self.test_status. setText(f"✅ 已发送按键 VK:  0x{vk_code: 02X}")
        self.test_status.setStyleSheet("color: blue; padding: 10px; font-weight: bold;")
    
    def test_send_key(self):
        """测试发送自定义按键"""
        if not self.input_controller:
            self.show_error("请先选择游戏窗口！")
            return
        
        vk_text = self.vk_input. text().strip()
        if not vk_text:
            self.show_error("请输入虚拟键码！")
            return
        
        try:
            # 支持 0x57 或 57 格式
            vk_code = int(vk_text, 16) if vk_text.startswith('0x') else int(vk_text)
            self.send_key(vk_code)
        except ValueError:
            self.show_error("无效的虚拟键码格式！")
    
    def test_screenshot(self):
        """测试截图"""
        if not self.window_manager. current_hwnd:
            self.show_error("请先选择游戏窗口！")
            return
        
        from core.screen_capture import ScreenCapture
        
        try:
            capturer = ScreenCapture(self.window_manager.current_hwnd)
            filename = "screenshot. png"
            capturer.save_screenshot(filename)
            self.screenshot_label.setText(f"✅ 截图已保存到：{filename}")
            self.screenshot_label.setStyleSheet("padding: 5px; color: green;")
        except Exception as e:
            self.show_error(f"截图失败：{str(e)}")
    
    def show_error(self, message):
        """显示错误消息"""
        self.test_status.setText(f"❌ {message}")
        self.test_status.setStyleSheet("color: red; padding: 10px; font-weight: bold;")
"""
主窗口 - 可视化操作台（增强版）
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QTextEdit, QGroupBox, 
                              QDialog, QListWidget, QListWidgetItem, QMessageBox,
                              QTabWidget)  # 新增
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.window_manager import WindowManager, WindowInfo
from gui.test_panel import TestPanel  # 新增

class WindowSelectDialog(QDialog):
    """窗口选择对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_hwnd = None
        self.window_manager = WindowManager()
        self.init_ui()
        self.refresh_windows()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("🔍 选择游戏窗口")
        self.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout(self)
        
        info_label = QLabel("请从下方列表中选择游戏窗口：")
        info_label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(info_label)
        
        self.window_list = QListWidget()
        self.window_list.itemDoubleClicked.connect(self. on_window_selected)
        layout.addWidget(self.window_list)
        
        button_layout = QHBoxLayout()
        
        self.btn_refresh = QPushButton("🔄 刷新列表")
        self.btn_refresh.clicked.connect(self. refresh_windows)
        button_layout.addWidget(self.btn_refresh)
        
        button_layout.addStretch()
        
        self.btn_select = QPushButton("✅ 选择")
        self.btn_select.clicked. connect(self.on_select_clicked)
        self.btn_select.setEnabled(False)
        button_layout. addWidget(self.btn_select)
        
        self.btn_cancel = QPushButton("❌ 取消")
        self.btn_cancel.clicked. connect(self.reject)
        button_layout.addWidget(self. btn_cancel)
        
        layout.addLayout(button_layout)
        
        self.window_list.itemSelectionChanged.connect(self.on_selection_changed)
    
    def refresh_windows(self):
        """刷新窗口列表"""
        self.window_list.clear()
        windows = self.window_manager.get_all_windows()
        
        if not windows:
            item = QListWidgetItem("❌ 未检测到任何窗口")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.window_list.addItem(item)
            return
        
        for window in windows:
            display_text = f"[{window.hwnd}] {window.title}"
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, window.hwnd)
            
            if any(keyword in window.title.lower() for keyword in 
                   ['game', 'unity', 'unreal', 'directx', 'opengl']):
                font = QFont()
                font. setBold(True)
                item. setFont(font)
            
            self.window_list.addItem(item)
    
    def on_selection_changed(self):
        """选择变化时"""
        self.btn_select.setEnabled(len(self.window_list.selectedItems()) > 0)
    
    def on_select_clicked(self):
        """点击选择按钮"""
        selected_items = self.window_list.selectedItems()
        if selected_items:
            self.selected_hwnd = selected_items[0].data(Qt.ItemDataRole.UserRole)
            self.accept()
    
    def on_window_selected(self, item):
        """双击窗口项"""
        self.selected_hwnd = item. data(Qt.ItemDataRole. UserRole)
        self.accept()


class MainWindow(QMainWindow):
    """主控制台窗口"""
    
    def __init__(self):
        super().__init__()
        self.window_manager = WindowManager()
        self.game_hwnd = None
        self.worker_thread = None
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("🎮 游戏自动化控制台 v1.0")
        self.setGeometry(100, 100, 950, 750)
        
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                padding: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        
        # ========== 窗口信息组 ==========
        window_group = QGroupBox("🪟 游戏窗口信息")
        window_layout = QVBoxLayout()
        
        self.window_status_label = QLabel("状态：未选择游戏窗口")
        self.window_status_label. setStyleSheet("color: red; font-size: 13px; padding: 5px;")
        window_layout.addWidget(self.window_status_label)
        
        self. window_info_label = QLabel("窗口信息：无")
        self.window_info_label.setStyleSheet("padding: 5px; background-color: #f5f5f5; border-radius: 3px;")
        window_layout.addWidget(self.window_info_label)
        
        btn_layout = QHBoxLayout()
        
        self.btn_detect = QPushButton("🔍 选择游戏窗口")
        self.btn_detect.clicked. connect(self.detect_window)
        self.btn_detect.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_layout.addWidget(self.btn_detect)
        
        self.btn_refresh = QPushButton("🔄 刷新窗口信息")
        self.btn_refresh.clicked.connect(self. refresh_window_info)
        self.btn_refresh.setEnabled(False)
        btn_layout.addWidget(self. btn_refresh)
        
        self.btn_activate = QPushButton("📌 激活窗口")
        self.btn_activate.clicked.connect(self.activate_game_window)
        self.btn_activate.setEnabled(False)
        btn_layout.addWidget(self.btn_activate)
        
        window_layout.addLayout(btn_layout)
        window_group.setLayout(window_layout)
        main_layout.addWidget(window_group)
        
        # ========== 标签页切换器 ==========
        self.tab_widget = QTabWidget()
        
        # 主控制页
        main_tab = QWidget()
        main_tab_layout = QVBoxLayout(main_tab)
        
        # 控制按钮组
        control_group = QGroupBox("⚙️ 控制面板")
        control_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("▶️ 启动自动化")
        self.btn_start.clicked.connect(self.start_automation)
        self.btn_start.setEnabled(False)
        self.btn_start.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px;")
        control_layout.addWidget(self.btn_start)
        
        self. btn_stop = QPushButton("⏹️ 停止自动化")
        self.btn_stop.clicked.connect(self.stop_automation)
        self.btn_stop.setEnabled(False)
        self.btn_stop. setStyleSheet("background-color:  #f44336; color: white; font-size: 14px;")
        control_layout. addWidget(self.btn_stop)
        
        control_group.setLayout(control_layout)
        main_tab_layout.addWidget(control_group)
        
        # 状态信息组
        status_group = QGroupBox("📊 运行状态")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("当前状态：待机中")
        self.status_label.setStyleSheet("font-size: 13px; padding: 5px;")
        status_layout.addWidget(self.status_label)
        
        status_group.setLayout(status_layout)
        main_tab_layout. addWidget(status_group)
        
        # 日志显示
        log_group = QGroupBox("📋 运行日志")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family:  Consolas;")
        log_layout.addWidget(self. log_text)
        
        self.btn_clear_log = QPushButton("🗑️ 清空日志")
        self.btn_clear_log.clicked.connect(self. log_text.clear)
        log_layout.addWidget(self. btn_clear_log)
        
        log_group.setLayout(log_layout)
        main_tab_layout.addWidget(log_group)
        
        # 测试页
        self.test_panel = TestPanel(self.window_manager)
        
        # 添加标签页
        self.tab_widget.addTab(main_tab, "🎯 主控制台")
        self.tab_widget.addTab(self.test_panel, "🧪 功能测试")
        
        main_layout.addWidget(self.tab_widget)
        
        # 初始日志
        self.log("✅ 程序已启动，请先选择游戏窗口")
    
    def detect_window(self):
        """打开窗口选择对话框"""
        self.log("🔍 正在检测游戏窗口...")
        
        dialog = WindowSelectDialog(self)
        if dialog.exec() == QDialog.DialogCode. Accepted:
            hwnd = dialog.selected_hwnd
            if hwnd:
                if self.window_manager.select_window(hwnd):
                    self.game_hwnd = hwnd
                    self.update_window_info()
                    self.log(f"✅ 成功绑定窗口：{self.window_manager.get_window_title(hwnd)} [hwnd: {hwnd}]")
                    
                    # 更新测试面板的控制器
                    self.test_panel.update_controller(hwnd)
                    
                    self.btn_refresh.setEnabled(True)
                    self.btn_activate.setEnabled(True)
                    self.btn_start.setEnabled(True)
                else:
                    self.log("❌ 窗口绑定失败，请重新选择")
                    QMessageBox.warning(self, "错误", "窗口绑定失败！")
        else:
            self.log("⚠️ 取消选择窗口")
    
    def update_window_info(self):
        """更新窗口信息显示"""
        if not self.game_hwnd:
            return
        
        info = self.window_manager.get_current_window_info()
        if info:
            self.window_status_label.setText("状态：已连接 ✅")
            self.window_status_label.setStyleSheet("color: green; font-size: 13px; padding: 5px;")
            
            x, y, w, h = info. rect
            info_text = f"窗口句柄：{info.hwnd}\n"
            info_text += f"窗口标题：{info.title}\n"
            info_text += f"窗口类名：{info.class_name}\n"
            info_text += f"窗口位置：({x}, {y})  大小：{w} x {h}"
            
            self.window_info_label.setText(info_text)
        else:
            self.window_status_label.setText("状态：窗口已失效 ❌")
            self.window_status_label.setStyleSheet("color: red; font-size: 13px; padding: 5px;")
            self.window_info_label. setText("窗口信息：无")
            self.game_hwnd = None
            self.test_panel.update_controller(None)
            self.btn_refresh.setEnabled(False)
            self.btn_activate.setEnabled(False)
            self.btn_start.setEnabled(False)
    
    def refresh_window_info(self):
        """刷新窗口信息"""
        self.log("🔄 刷新窗口信息...")
        self.update_window_info()
    
    def activate_game_window(self):
        """激活游戏窗口"""
        if self.game_hwnd:
            if self.window_manager.activate_window(self.game_hwnd):
                self.log("📌 游戏窗口已激活")
            else:
                self.log("❌ 激活窗口失败")
                QMessageBox.warning(self, "错误", "无法激活窗口！")
    
    def start_automation(self):
        """启动自动化"""
        self.log("▶️ 启动自动化流程...")
        self.status_label.setText("当前状态：运行中 🟢")
        self.btn_start.setEnabled(False)
        self.btn_stop. setEnabled(True)
        self.btn_detect.setEnabled(False)
    
    def stop_automation(self):
        """停止自动化"""
        self.log("⏹️ 停止自动化流程...")
        self.status_label.setText("当前状态：已停止 🔴")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_detect.setEnabled(True)
    
    def log(self, message):
        """添加日志"""
        from datetime import datetime
        timestamp = datetime. now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
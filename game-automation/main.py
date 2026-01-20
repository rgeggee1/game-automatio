"""
游戏自动化辅助程序 - 主入口
"""
import sys
import os

# 确保导入路径正确
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """主函数"""
    # 创建GUI应用
    app = QApplication(sys. argv)
    
    # 设置应用信息
    app.setApplicationName("游戏自动化助手")
    app.setOrganizationName("GameAutomation")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__": 
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
学生信息管理系统 - 主程序入口
"""

import os
import sys
from datetime import datetime

# 确保可以导入自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.managers.data_manager import DataManager
from src.managers.student_manager import StudentManager
from src.ui.user_interface import UserInterface
from src.utils.logger import logger
from src.utils.exceptions import handle_exception, safe_operation


class StudentManagementSystem:
    """学生信息管理系统主类"""
    
    def __init__(self):
        """初始化系统"""
        self.data_manager = None
        self.student_manager = None
        self.user_interface = None
        self.is_running = False
        
    @safe_operation(logger)
    def initialize(self):
        """初始化系统各组件"""
        logger.info("正在初始化学生信息管理系统...")
        
        # 创建数据管理器实例
        self.data_manager = DataManager()
        logger.info("数据管理器初始化完成")
        
        # 创建学生管理器实例
        self.student_manager = StudentManager(self.data_manager)
        logger.info("学生管理器初始化完成")
        
        # 创建用户界面实例
        self.user_interface = UserInterface(self.student_manager)
        logger.info("用户界面初始化完成")
        
        # 注意：StudentManager在初始化时已经自动加载了数据
        logger.info("系统数据加载完成")
        
        return True
    
    @safe_operation(logger)
    def start(self):
        """启动系统"""
        if not self.initialize():
            logger.error("系统初始化失败，无法启动")
            return False
        
        self.is_running = True
        logger.info("学生信息管理系统启动成功")
        
        try:
            # 显示欢迎信息
            self.user_interface.print_title("欢迎使用学生信息管理系统")
            
            # 进入主菜单循环
            while self.is_running:
                self.user_interface.show_main_menu()
                choice = self.user_interface.get_input("请输入您的选择: ")
                self.handle_main_menu_choice(choice)
        
        except KeyboardInterrupt:
            logger.warning("用户中断操作")
            print("\n程序已被用户中断。")
        
        finally:
            self.shutdown()
        
        return True
    
    def handle_main_menu_choice(self, choice):
        """处理主菜单选择"""
        if choice == '1':
            # 学生信息管理
            self.user_interface.student_management_menu()
        elif choice == '2':
            # 班级管理
            self.user_interface.class_management_menu()
        elif choice == '3':
            # 数据导入导出
            self.user_interface.data_import_export_menu()
        elif choice == '4':
            # 数据备份恢复
            self.user_interface.backup_restore_menu()
        elif choice == '5':
            # 系统信息
            self.display_system_info()
        elif choice == '0':
            # 退出系统
            self.is_running = False
            logger.info("用户选择退出系统")
            print("感谢使用学生信息管理系统！再见！")
        else:
            print("无效的选择，请重新输入。")
            logger.warning(f"用户输入无效选项: {choice}")
    
    def display_system_info(self):
        """显示系统信息"""
        print("\n=== 系统信息 ===")
        print(f"系统名称: 学生信息管理系统")
        print(f"当前版本: 1.0.0")
        print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"学生总数: {len(self.student_manager.get_all_students())}")
        print(f"班级数量: {len(self.student_manager.get_all_classes())}")
        print(f"数据文件: {self.data_manager.data_file}")
        print("================\n")
        logger.info("显示系统信息")
    
    @safe_operation(logger)
    def shutdown(self):
        """关闭系统并清理资源"""
        if self.is_running or self.student_manager:
            logger.info("正在关闭学生信息管理系统...")
            
            # 保存数据 - 注意：在StudentManager类中，数据变更时会自动保存，这里不需要额外调用
            
            # 清理资源
            self.is_running = False
            
            logger.info("学生信息管理系统已安全关闭")


def main():
    """程序主入口"""
    # 捕获全局异常
    try:
        # 创建系统实例
        system = StudentManagementSystem()
        
        # 启动系统
        system.start()
        
    except Exception as e:
        handle_exception(e, logger)
        print("系统发生严重错误，请联系管理员。")
    
    finally:
        logger.info("程序执行完毕")


if __name__ == "__main__":
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
学生信息管理系统 - 启动脚本
"""

import os
import sys

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 添加项目根目录到 Python 路径
sys.path.append(script_dir)

# 导入主程序并运行
if __name__ == "__main__":
    try:
        # 直接运行主程序
        from src.main import main
        main()
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保项目结构正确，并且所有依赖已安装。")
    except Exception as e:
        print(f"运行错误: {e}")
    finally:
        input("\n按回车键退出...")
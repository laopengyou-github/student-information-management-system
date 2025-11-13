#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试运行器 - 确保正确设置Python路径并运行测试
"""

import os
import sys
import unittest

# 添加项目根目录和src目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# 修改sys.modules确保正确导入
sys.modules.pop('src.models.student', None)
sys.modules.pop('src.managers.data_manager', None)
sys.modules.pop('src.managers.student_manager', None)

# 导入所有测试模块
from tests.test_student import TestStudent
from tests.test_data_manager import TestDataManager
from tests.test_student_manager import TestStudentManager

if __name__ == '__main__':
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_suite.addTest(unittest.makeSuite(TestStudent))
    test_suite.addTest(unittest.makeSuite(TestDataManager))
    test_suite.addTest(unittest.makeSuite(TestStudentManager))
    
    # 运行测试
    print("开始运行测试...")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出测试结果摘要
    print("\n测试结果摘要:")
    print(f"运行测试总数: {result.testsRun}")
    print(f"失败测试数: {len(result.failures)}")
    print(f"错误测试数: {len(result.errors)}")
    print(f"跳过测试数: {len(result.skipped)}")
    
    # 根据测试结果设置退出码
    sys.exit(not result.wasSuccessful())
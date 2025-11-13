#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试学生管理器模块(StudentManager)功能
"""

import unittest
import sys
import os
import shutil

# 添加项目根目录和src目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from managers.student_manager import StudentManager
from managers.data_manager import DataManager
from utils.exceptions import StudentNotFoundError, DataValidationError, StudentAlreadyExistsError


class TestStudentManager(unittest.TestCase):
    """学生管理器测试用例"""
    
    def setUp(self):
        """每个测试用例执行前的设置"""
        # 创建测试用的数据目录
        self.test_data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'tests', 'test_data'
        )
        # 清空测试数据目录，确保每次测试都是干净的环境
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        os.makedirs(self.test_data_dir)
        
        # 创建测试用的数据文件路径
        self.test_data_file = os.path.join(self.test_data_dir, 'test_students.json')
        self.test_backup_dir = os.path.join(self.test_data_dir, 'backups')
        
        # 创建数据管理器实例
        self.data_manager = DataManager(
            data_file=self.test_data_file
        )
        
        # 创建学生管理器实例，传入自定义的数据管理器
        self.student_manager = StudentManager(data_manager=self.data_manager)
        
        # 添加测试数据
        self.student_manager.add_student(
            student_id="2023001",
            name="张三",
            gender="男",
            age=20,
            class_name="计算机科学与技术1班",
            contact="13800138001"
        )
        
        self.student_manager.add_student(
            student_id="2023002",
            name="李四",
            gender="女",
            age=21,
            class_name="计算机科学与技术1班",
            contact="13800138002"
        )
        
        self.student_manager.add_student(
            student_id="2023003",
            name="王五",
            gender="男",
            age=22,
            class_name="计算机科学与技术2班",
            contact="13800138003"
        )
    
    def tearDown(self):
        """每个测试用例执行后的清理"""
        # 清理测试数据文件
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        
        # 清理测试备份目录
        if os.path.exists(self.test_backup_dir):
            shutil.rmtree(self.test_backup_dir)
        
        # 清理测试数据目录
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
    
    def test_add_student(self):
        """测试添加学生"""
        # 获取当前学生数量
        initial_count = len(self.student_manager.get_all_students())
        
        # 添加新学生，使用不同的学号避免与初始数据冲突
        self.student_manager.add_student(
            student_id="2023004",
            name="赵六",
            gender="男",
            age=23,
            class_name="计算机科学与技术2班",
            contact="13800138004"
        )
        
        # 验证学生数量增加
        self.assertEqual(len(self.student_manager.get_all_students()), initial_count + 1)
        
        # 验证新学生信息正确
        new_student = self.student_manager.get_student_by_id("2023004")
        self.assertIsNotNone(new_student)
        self.assertEqual(new_student.name, "赵六")
        
        # 测试添加重复学号的学生
        with self.assertRaises(StudentAlreadyExistsError):
            self.student_manager.add_student(
                student_id="2023001",  # 重复的学号
                name="重复学生",
                gender="男",
                age=20,
                class_name="计算机科学与技术1班",
                contact="13800138005"
            )
    
    def test_search_student_by_id(self):
        """测试按学号搜索学生"""
        # 搜索存在的学生
        student = self.student_manager.get_student_by_id("2023001")
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "张三")
        
        # 搜索不存在的学生
        with self.assertRaises(StudentNotFoundError):
            self.student_manager.get_student_by_id("999999")
    
    def test_search_students_by_name(self):
        """测试按姓名搜索学生"""
        # 添加一个姓名相似的学生
        self.student_manager.add_student(
            student_id="2023005",
            name="张三丰",
            gender="男",
            age=24,
            class_name="计算机科学与技术3班",
            contact="13800138005"
        )
        
        # 按姓名模糊搜索
        results = self.student_manager.search_students_by_name("张")
        self.assertEqual(len(results), 2)  # 应该找到张三和张三丰
        
        # 搜索不存在的姓名
        results = self.student_manager.search_students_by_name("不存在的姓名")
        self.assertEqual(len(results), 0)
    
    def test_search_students_by_class(self):
        """测试按班级搜索学生"""
        # 按班级搜索
        results = self.student_manager.search_students_by_class("计算机科学与技术1班")
        self.assertEqual(len(results), 2)  # 应该找到张三和李四
        
        # 搜索不存在的班级
        results = self.student_manager.search_students_by_class("不存在的班级")
        self.assertEqual(len(results), 0)
    
    def test_update_student(self):
        """测试更新学生信息"""
        # 更新学生信息
        self.student_manager.update_student(
            student_id="2023001",
            name="张三改",
            age=25,
            contact="13900139001"
        )
        
        # 验证更新成功
        updated_student = self.student_manager.get_student_by_id("2023001")
        self.assertEqual(updated_student.name, "张三改")
        self.assertEqual(updated_student.age, 25)
        self.assertEqual(updated_student.contact, "13900139001")
        
        # 测试更新不存在的学生
        with self.assertRaises(StudentNotFoundError):
            self.student_manager.update_student(
                student_id="999999",
                name="不存在的学生",
                age=20
            )
    
    def test_delete_student(self):
        """测试删除学生"""
        # 获取当前学生数量
        initial_count = len(self.student_manager.get_all_students())
        
        # 删除学生
        self.student_manager.delete_student("2023001")
        
        # 验证学生数量减少
        self.assertEqual(len(self.student_manager.get_all_students()), initial_count - 1)
        
        # 验证学生已被删除
        with self.assertRaises(StudentNotFoundError):
            self.student_manager.get_student_by_id("2023001")
        
        # 测试删除不存在的学生
        with self.assertRaises(StudentNotFoundError):
            self.student_manager.delete_student("999999")
    
    def test_batch_delete_students(self):
        """测试批量删除学生"""
        # 获取当前学生数量
        initial_count = len(self.student_manager.get_all_students())
        
        # 批量删除学生
        deleted_count = self.student_manager.delete_students_by_ids(["2023001", "2023002"])
        
        # 验证删除数量正确，注意返回值是元组格式
        self.assertEqual(deleted_count[0], 2)
        
        # 验证学生数量减少
        self.assertEqual(len(self.student_manager.get_all_students()), initial_count - 2)
        
        # 验证学生已被删除
        with self.assertRaises(StudentNotFoundError):
            self.student_manager.get_student_by_id("2023001")
    
    def test_get_all_classes(self):
        """测试获取所有班级"""
        classes = self.student_manager.get_class_list()
        self.assertIn("计算机科学与技术1班", classes)
        self.assertIn("计算机科学与技术2班", classes)
        self.assertEqual(len(classes), 2)
    
    def test_get_students_count_by_class(self):
        """测试获取班级学生数量"""
        count = self.student_manager.get_class_student_count("计算机科学与技术1班")
        self.assertEqual(count, 2)
        
        # 测试不存在的班级
        count = self.student_manager.get_class_student_count("不存在的班级")
        self.assertEqual(count, 0)
    
    def test_save_and_load_data(self):
        """测试保存和加载数据"""
        # 添加一个新学生
        self.student_manager.add_student(
            student_id="2023006",
            name="测试保存",
            gender="男",
            age=26,
            class_name="测试班级",
            contact="13800138006"
        )
        
        # 添加操作会自动保存数据，这里不需要额外调用save_data
        
        # 创建新的学生管理器实例，初始化时会自动加载数据
        new_student_manager = StudentManager(self.data_manager)
        
        # 验证数据是否正确加载
        loaded_student = new_student_manager.get_student_by_id("2023006")
        self.assertIsNotNone(loaded_student)
        self.assertEqual(loaded_student.name, "测试保存")


if __name__ == '__main__':
    unittest.main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试学生类(Student)功能
"""

import unittest
import sys
import os

# 添加项目根目录和src目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from models.student import Student
from utils.exceptions import DataValidationError


class TestStudent(unittest.TestCase):
    """学生类测试用例"""
    
    def setUp(self):
        """每个测试用例执行前的设置"""
        # 创建一个有效的学生对象用于测试
        self.valid_student = Student(
            student_id="2023001",
            name="张三",
            gender="男",
            age=20,
            class_name="计算机科学与技术1班",
            contact="13800138001"
        )
    
    def test_valid_student_creation(self):
        """测试创建有效的学生对象"""
        # 验证创建的学生对象属性值正确
        self.assertEqual(self.valid_student.student_id, "2023001")
        self.assertEqual(self.valid_student.name, "张三")
        self.assertEqual(self.valid_student.gender, "男")
        self.assertEqual(self.valid_student.age, 20)
        self.assertEqual(self.valid_student.class_name, "计算机科学与技术1班")
        self.assertEqual(self.valid_student.contact, "13800138001")
    
    def test_invalid_student_id(self):
        """测试无效的学号"""
        # 测试空学号
        with self.assertRaises(DataValidationError):
            Student(
                student_id="",
                name="张三",
                gender="男",
                age=20,
                class_name="计算机科学与技术1班",
                contact="13800138001"
            )
        
        # 测试非法格式学号
        with self.assertRaises(DataValidationError):
            Student(
                student_id="abc123",
                name="张三",
                gender="男",
                age=20,
                class_name="计算机科学与技术1班",
                contact="13800138001"
            )
    
    def test_invalid_name(self):
        """测试无效的姓名"""
        # 测试空姓名
        with self.assertRaises(DataValidationError):
            Student(
                student_id="2023001",
                name="",
                gender="男",
                age=20,
                class_name="计算机科学与技术1班",
                contact="13800138001"
            )
        
        # 测试过长姓名
        with self.assertRaises(DataValidationError):
            Student(
                student_id="2023001",
                name="这是一个超过20个字符的非常长的姓名",
                gender="男",
                age=20,
                class_name="计算机科学与技术1班",
                contact="13800138001"
            )
    
    def test_invalid_gender(self):
        """测试无效的性别"""
        # 测试非法性别值
        with self.assertRaises(DataValidationError):
            Student(
                student_id="2023001",
                name="张三",
                gender="未知",
                age=20,
                class_name="计算机科学与技术1班",
                contact="13800138001"
            )
    
    def test_invalid_age(self):
        """测试无效的年龄"""
        # 测试年龄过小
        with self.assertRaises(DataValidationError):
            Student(
                student_id="2023001",
                name="张三",
                gender="男",
                age=10,
                class_name="计算机科学与技术1班",
                contact="13800138001"
            )
        
        # 测试年龄过大
        with self.assertRaises(DataValidationError):
            Student(
                student_id="2023001",
                name="张三",
                gender="男",
                age=50,
                class_name="计算机科学与技术1班",
                contact="13800138001"
            )
    
    def test_invalid_contact(self):
        """测试无效的联系方式"""
        # 测试非法手机号
        with self.assertRaises(DataValidationError):
            Student(
                student_id="2023001",
                name="张三",
                gender="男",
                age=20,
                class_name="计算机科学与技术1班",
                contact="123456"
            )
    
    def test_update_student_info(self):
        """测试更新学生信息"""
        # 更新学生信息
        self.valid_student.name = "李四"
        self.valid_student.age = 21
        self.valid_student.contact = "13900139001"
        
        # 验证更新后的值正确
        self.assertEqual(self.valid_student.name, "李四")
        self.assertEqual(self.valid_student.age, 21)
        self.assertEqual(self.valid_student.contact, "13900139001")
    
    def test_to_dict_and_from_dict(self):
        """测试学生对象与字典的相互转换"""
        # 转换为字典
        student_dict = self.valid_student.to_dict()
        
        # 验证字典包含所有必要的键值对
        required_keys = ['student_id', 'name', 'gender', 'age', 'class_name', 'contact']
        for key in required_keys:
            self.assertIn(key, student_dict)
        
        # 从字典创建新的学生对象
        new_student = Student.from_dict(student_dict)
        
        # 验证新对象与原对象属性一致
        self.assertEqual(new_student.student_id, self.valid_student.student_id)
        self.assertEqual(new_student.name, self.valid_student.name)
        self.assertEqual(new_student.gender, self.valid_student.gender)
        self.assertEqual(new_student.age, self.valid_student.age)
        self.assertEqual(new_student.class_name, self.valid_student.class_name)
        self.assertEqual(new_student.contact, self.valid_student.contact)
    
    def test_str_representation(self):
        """测试学生对象的字符串表示"""
        student_str = str(self.valid_student)
        
        # 验证字符串包含必要信息
        self.assertIn("2023001", student_str)
        self.assertIn("张三", student_str)
        self.assertIn("男", student_str)
        self.assertIn("计算机科学与技术1班", student_str)


if __name__ == '__main__':
    unittest.main()
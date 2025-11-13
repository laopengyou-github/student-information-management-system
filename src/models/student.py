"""
学生类模块
定义学生对象的基本属性和方法
"""
from src.utils.validator import Validator
from src.utils.exceptions import DataValidationError

class Student:
    """
    学生类
    表示一个学生对象，包含基本信息和相关操作方法
    """
    
    def __init__(self, student_id, name, gender, age, class_name, contact):
        """
        初始化学生对象
        
        Args:
            student_id: 学号
            name: 姓名
            gender: 性别
            age: 年龄
            class_name: 班级
            contact: 联系方式
            
        Raises:
            DataValidationError: 当数据验证失败时
        """
        # 创建验证器实例
        self._validator = Validator()
        
        # 验证并设置属性
        self._student_id = self._validate_student_id(student_id)
        self._name = self._validate_name(name)
        self._gender = self._validate_gender(gender)
        self._age = self._validate_age(age)
        self._class_name = self._validate_class_name(class_name)
        self._contact = self._validate_contact(contact)
    
    def _validate_student_id(self, student_id):
        """验证学号"""
        try:
            is_valid, error_msg = self._validator.validate_student_id(student_id)
            if not is_valid:
                raise DataValidationError(error_msg, "student_id")
            return student_id
        except Exception as e:
            if isinstance(e, DataValidationError):
                raise
            raise DataValidationError(str(e), "student_id")
    
    def _validate_name(self, name):
        """验证姓名"""
        try:
            is_valid, error_msg = self._validator.validate_name(name)
            if not is_valid:
                raise DataValidationError(error_msg, "name")
            return name.strip()
        except Exception as e:
            if isinstance(e, DataValidationError):
                raise
            raise DataValidationError(str(e), "name")
    
    def _validate_gender(self, gender):
        """验证性别"""
        try:
            is_valid, error_msg = self._validator.validate_gender(gender)
            if not is_valid:
                raise DataValidationError(error_msg, "gender")
            return gender
        except Exception as e:
            if isinstance(e, DataValidationError):
                raise
            raise DataValidationError(str(e), "gender")
    
    def _validate_age(self, age):
        """验证年龄"""
        try:
            is_valid, error_msg = self._validator.validate_age(age)
            if not is_valid:
                raise DataValidationError(error_msg, "age")
            return int(age)
        except Exception as e:
            if isinstance(e, DataValidationError):
                raise
            raise DataValidationError(str(e), "age")
    
    def _validate_class_name(self, class_name):
        """验证班级"""
        try:
            is_valid, error_msg = self._validator.validate_class_name(class_name)
            if not is_valid:
                raise DataValidationError(error_msg, "class_name")
            return class_name.strip()
        except Exception as e:
            if isinstance(e, DataValidationError):
                raise
            raise DataValidationError(str(e), "class_name")
    
    def _validate_contact(self, contact):
        """验证联系方式"""
        try:
            is_valid, error_msg = self._validator.validate_contact(contact)
            if not is_valid:
                raise DataValidationError(error_msg, "contact")
            return contact.strip()
        except Exception as e:
            if isinstance(e, DataValidationError):
                raise
            raise DataValidationError(str(e), "contact")
    
    @property
    def student_id(self):
        """获取学号"""
        return self._student_id
    
    @property
    def name(self):
        """获取姓名"""
        return self._name
    
    @name.setter
    def name(self, value):
        """设置姓名"""
        self._name = self._validate_name(value)
    
    @property
    def gender(self):
        """获取性别"""
        return self._gender
    
    @gender.setter
    def gender(self, value):
        """设置性别"""
        self._gender = self._validate_gender(value)
    
    @property
    def age(self):
        """获取年龄"""
        return self._age
    
    @age.setter
    def age(self, value):
        """设置年龄"""
        self._age = self._validate_age(value)
    
    @property
    def class_name(self):
        """获取班级"""
        return self._class_name
    
    @class_name.setter
    def class_name(self, value):
        """设置班级"""
        self._class_name = self._validate_class_name(value)
    
    @property
    def contact(self):
        """获取联系方式"""
        return self._contact
    
    @contact.setter
    def contact(self, value):
        """设置联系方式"""
        self._contact = self._validate_contact(value)
    
    def to_dict(self):
        """
        将学生对象转换为字典
        
        Returns:
            dict: 包含学生所有属性的字典
        """
        return {
            'student_id': self._student_id,
            'name': self._name,
            'gender': self._gender,
            'age': self._age,
            'class_name': self._class_name,
            'contact': self._contact
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        从字典创建学生对象
        
        Args:
            data: 包含学生信息的字典
            
        Returns:
            Student: 学生对象
            
        Raises:
            DataValidationError: 当数据验证失败时
        """
        try:
            return cls(
                student_id=data.get('student_id'),
                name=data.get('name'),
                gender=data.get('gender'),
                age=data.get('age'),
                class_name=data.get('class_name'),
                contact=data.get('contact')
            )
        except KeyError as e:
            raise DataValidationError(f"缺少必要字段: {str(e)}", "data_incomplete")
    
    def update_info(self, **kwargs):
        """
        更新学生信息
        
        Args:
            **kwargs: 要更新的属性和值，支持name, gender, age, class_name, contact
            
        Returns:
            bool: 更新是否成功
            
        Raises:
            DataValidationError: 当数据验证失败时
            InvalidOperationError: 当尝试更新不允许修改的字段时
        """
        # 定义可更新的字段列表
        allowed_fields = ['name', 'gender', 'age', 'class_name', 'contact']
        has_changes = False
        
        # 检查并导入需要的异常
        from src.utils.exceptions import InvalidOperationError
        
        # 验证并更新字段
        for key, value in kwargs.items():
            # 不允许更新学号
            if key == 'student_id':
                raise InvalidOperationError("学号不允许修改")
            
            # 检查字段是否允许更新
            if key not in allowed_fields:
                raise DataValidationError(f"不允许更新字段: {key}", key)
            
            # 跳过None值更新
            if value is None:
                continue
            
            # 检查字段是否存在
            if hasattr(self, key):
                # 通过属性设置器进行更新（会自动验证）
                current_value = getattr(self, key)
                setattr(self, key, value)
                has_changes = True
            else:
                raise DataValidationError(f"学生对象不包含字段: {key}", key)
        
        return has_changes
    
    def __str__(self):
        """学生对象的字符串表示"""
        return f"学号: {self._student_id}, 姓名: {self._name}, 性别: {self._gender}, " \
               f"年龄: {self._age}, 班级: {self._class_name}, 联系方式: {self._contact}"
    
    def __repr__(self):
        """学生对象的正式字符串表示"""
        return f"Student(student_id='{self._student_id}', name='{self._name}', " \
               f"gender='{self._gender}', age={self._age}, class_name='{self._class_name}', " \
               f"contact='{self._contact}')"
    
    def __eq__(self, other):
        """判断两个学生对象是否相等（基于学号）"""
        if not isinstance(other, Student):
            return False
        return self._student_id == other._student_id
    
    def __hash__(self):
        """学生对象的哈希值（基于学号）"""
        return hash(self._student_id)
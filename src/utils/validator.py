import re

class Validator:
    """
    数据验证器类，用于验证各种输入数据的合法性
    提供学号、姓名、性别、年龄、班级、联系方式等字段的验证
    """
    
    @staticmethod
    def validate_student_id(student_id):
        """
        验证学号
        学号必须是数字格式，长度为6-20位
        
        Args:
            student_id: 学号
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if not isinstance(student_id, str):
            return False, "学号必须是字符串类型"
        
        if not student_id.strip():
            return False, "学号不能为空"
        
        # 修改为必须是数字且长度为6-20位
        if len(student_id) < 6 or len(student_id) > 20:
            return False, "学号长度必须在6-20位之间"
        
        # 使用正则表达式验证格式，只允许数字
        pattern = r'^[0-9]+$'
        if not re.match(pattern, student_id):
            return False, "学号格式不正确，应为数字且长度在6-20位之间"
        
        return True, ""
    
    @staticmethod
    def validate_name(name):
        """
        验证姓名
        姓名不能为空，长度在2-10个字符之间，支持中文姓名
        
        Args:
            name: 姓名
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if not isinstance(name, str):
            return False, "姓名必须是字符串类型"
        
        name = name.strip()
        if not name:
            return False, "姓名不能为空"
        
        if len(name) < 2 or len(name) > 10:
            return False, "姓名长度必须在2-10个字符之间"
        
        # 支持中文姓名，以及可能的英文姓名（包含空格）
        # 中文姓名：2-4个汉字
        # 英文姓名：名字+空格+姓氏，总长度不超过10
        chinese_pattern = r'^[\u4e00-\u9fa5]{2,10}$'
        english_pattern = r'^[a-zA-Z]+(\s[a-zA-Z]+)*$'
        
        if re.match(chinese_pattern, name) or re.match(english_pattern, name):
            return True, ""
        else:
            return False, "姓名格式不正确，只支持中文或英文姓名"
    
    @staticmethod
    def validate_gender(gender):
        """
        验证性别
        性别只能是'男'或'女'
        
        Args:
            gender: 性别
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if gender not in ['男', '女']:
            return False, "性别必须为'男'或'女'"
        
        return True, ""
    
    @staticmethod
    def validate_age(age):
        """
        验证年龄
        年龄必须是15-49之间的整数
        
        Args:
            age: 年龄
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        try:
            age = int(age)
        except (ValueError, TypeError):
            return False, "年龄必须是整数"
        
        if age < 15 or age >= 50:
            return False, "年龄必须是15-49之间的整数"
        
        return True, ""
    @staticmethod
    def validate_class_name(class_name):
        """
        验证班级名称
        班级名称不能为空，长度在1-20个字符之间
        
        Args:
            class_name: 班级名称
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if not isinstance(class_name, str):
            return False, "班级名称必须是字符串类型"
        
        class_name = class_name.strip()
        if not class_name:
            return False, "班级名称不能为空"
        
        if len(class_name) > 20:
            return False, "班级名称长度不能超过20个字符"
        
        # 班级名称可以包含汉字、字母、数字和常见符号（如2023级计算机1班）
        pattern = r'^[\u4e00-\u9fa5a-zA-Z0-9\s\-_]+$'
        if not re.match(pattern, class_name):
            return False, "班级名称包含非法字符"
        
        return True, ""
    
    @staticmethod
    def validate_contact(contact):
        """
        验证联系方式
        只支持中国大陆手机号或标准邮箱格式
        
        Args:
            contact: 联系方式
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if not isinstance(contact, str):
            return False, "联系方式必须是字符串类型"
        
        contact = contact.strip()
        if not contact:
            return False, "联系方式不能为空"
        
        if len(contact) > 50:
            return False, "联系方式长度不能超过50个字符"
        
        # 严格验证手机号格式（中国大陆手机号）
        phone_pattern = r'^1[3-9]\d{9}$'
        # 严格验证邮箱格式
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # 只接受标准手机号或邮箱格式
        if re.match(phone_pattern, contact) or re.match(email_pattern, contact):
            return True, ""
        else:
            return False, "联系方式格式不正确，应为手机号或邮箱"
    
    @staticmethod
    def validate_student_data(student_data):
        """
        验证学生数据的完整性和有效性
        
        Args:
            student_data: 包含学生信息的字典
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        # 检查必需字段
        required_fields = ['student_id', 'name', 'gender', 'age', 'class_name', 'contact']
        for field in required_fields:
            if field not in student_data:
                return False, f"缺少必需字段: {field}"
        
        # 验证各个字段
        validations = {
            'student_id': Validator.validate_student_id,
            'name': Validator.validate_name,
            'gender': Validator.validate_gender,
            'age': Validator.validate_age,
            'class_name': Validator.validate_class_name,
            'contact': Validator.validate_contact
        }
        
        for field, validator_func in validations.items():
            is_valid, error_msg = validator_func(student_data[field])
            if not is_valid:
                return False, f"{field}验证失败: {error_msg}"
        
        return True, ""
    
    @staticmethod
    def validate_input_list(input_list, min_length=1, max_length=100):
        """
        验证输入列表
        
        Args:
            input_list: 输入的列表
            min_length: 最小长度
            max_length: 最大长度
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if not isinstance(input_list, list):
            return False, "输入必须是列表类型"
        
        if len(input_list) < min_length:
            return False, f"列表长度不能少于{min_length}个元素"
        
        if len(input_list) > max_length:
            return False, f"列表长度不能超过{max_length}个元素"
        
        # 检查列表中是否有空元素
        for i, item in enumerate(input_list):
            if not item or (isinstance(item, str) and not item.strip()):
                return False, f"列表中的第{i+1}个元素为空"
        
        return True, ""
    
    @staticmethod
    def sanitize_string(input_string, max_length=50):
        """
        清理和标准化字符串输入
        
        Args:
            input_string: 输入字符串
            max_length: 最大长度
            
        Returns:
            str: 清理后的字符串
        """
        if not isinstance(input_string, str):
            input_string = str(input_string)
        
        # 去除首尾空格
        input_string = input_string.strip()
        
        # 限制长度
        if len(input_string) > max_length:
            input_string = input_string[:max_length]
        
        return input_string
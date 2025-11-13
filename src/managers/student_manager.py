from src.models.student import Student
from src.managers.data_manager import DataManager
from src.utils.logger import logger
from src.utils.exceptions import (
    StudentNotFoundError,
    StudentAlreadyExistsError as StudentExistsError,
    DataValidationError,
    InvalidOperationError,
    DataIOError,
    OperationFailedError
)
import re

class StudentManager:
    """
    学生管理类，处理学生信息的核心业务逻辑
    包含添加、查询、修改、删除等功能
    集成了异常处理和日志记录功能
    """
    
    def __init__(self, data_manager=None):
        """
        初始化学生管理器
        加载现有数据
        
        Args:
            data_manager: 可选的数据管理器实例，如果不提供则创建默认实例
            
        Raises:
            SystemConfigError: 当系统配置错误时
            DataIOError: 当数据加载失败时
        """
        try:
            logger.info("初始化学生管理器")
            # 如果提供了data_manager参数，则使用它；否则创建默认实例
            self._data_manager = data_manager if data_manager else DataManager()
            self._students = {}
            self._load_students()
            logger.info(f"学生管理器初始化完成，当前共有 {len(self._students)} 名学生")
        except Exception as e:
            logger.error(f"初始化学生管理器失败: {e}")
            raise
    
    def _load_students(self):
        """
        从数据文件加载学生数据
        
        Raises:
            DataIOError: 当数据加载失败时
        """
        try:
            logger.info("开始加载学生数据")
            students_data = self._data_manager.load_data()
            
            loaded_count = 0
            for student_id, student_info in students_data.items():
                try:
                    student = Student.from_dict(student_info)
                    self._students[student_id] = student
                    loaded_count += 1
                except Exception as e:
                    logger.error(f"加载学号为 {student_id} 的学生数据失败: {e}")
                    # 继续加载其他学生数据，不因为单个错误而中断
            
            logger.info(f"学生数据加载完成，共加载 {loaded_count} 名学生")
        except Exception as e:
            logger.error(f"加载学生数据时发生错误: {e}")
            raise DataIOError(str(e), "加载学生数据", "加载")
    
    def _save_students(self):
        """
        保存学生数据到文件
        
        Returns:
            bool: 保存是否成功
            
        Raises:
            DataIOError: 当数据保存失败时
        """
        try:
            logger.debug(f"开始保存学生数据，共 {len(self._students)} 名学生")
            students_data = {}
            for student_id, student in self._students.items():
                try:
                    students_data[student_id] = student.to_dict()
                except Exception as e:
                    logger.error(f"序列化学号为 {student_id} 的学生数据失败: {e}")
                    raise DataValidationError(f"学生数据序列化失败: {str(e)}")
            
            success = self._data_manager.save_data(students_data)
            logger.debug(f"学生数据保存 {'成功' if success else '失败'}")
            return success
        except Exception as e:
            logger.error(f"保存学生数据时发生错误: {e}")
            # 如果是我们自定义的异常，则直接抛出
            if isinstance(e, (DataIOError, DataValidationError)):
                raise
            # 否则包装为DataIOError
            raise DataIOError(str(e), "保存学生数据", "保存")
    
    def add_student(self, student_id, name, gender, age, class_name, contact):
        """
        添加学生信息
        
        Args:
            student_id: 学号
            name: 姓名
            gender: 性别
            age: 年龄
            class_name: 班级
            contact: 联系方式
            
        Returns:
            tuple: (是否成功, 消息)
            
        Raises:
            DataValidationError: 当数据验证失败时
            StudentExistsError: 当学生已存在时
            DataIOError: 当数据保存失败时
        """
        try:
            # 验证学号格式
            if not self._validate_student_id(student_id):
                error_msg = "学号格式不正确，应为字母、数字和下划线组合，长度3-20个字符"
                logger.warning(f"添加学生失败 - {error_msg}")
                raise DataValidationError(error_msg)
            
            # 检查学号是否已存在
            if student_id in self._students:
                error_msg = f"学号 {student_id} 已存在"
                logger.warning(f"添加学生失败 - {error_msg}")
                raise StudentExistsError(student_id)
            
            # 记录添加操作
            logger.info(f"添加学生: 学号={student_id}, 姓名={name}, 班级={class_name}")
            
            # 创建学生对象
            try:
                student = Student(
                    student_id=student_id,
                    name=name,
                    gender=gender,
                    age=int(age),
                    class_name=class_name,
                    contact=contact
                )
            except ValueError as e:
                logger.error(f"创建学生对象失败: {e}")
                raise DataValidationError(str(e))
            
            # 添加到学生字典
            self._students[student_id] = student
            
            # 保存数据
            try:
                self._save_students()
                success_msg = f"学生 {name} 添加成功"
                logger.info(success_msg)
                return True, success_msg
            except Exception:
                # 如果保存失败，从内存中移除学生
                if student_id in self._students:
                    del self._students[student_id]
                logger.error("保存数据失败，撤销添加操作")
                raise
                
        except (DataValidationError, StudentExistsError, DataIOError):
            # 直接向上抛出这些特定异常
            raise
        except Exception as e:
            logger.error(f"添加学生失败: {e}")
            raise OperationFailedError(f"添加学生失败: {str(e)}")
    
    def get_student_by_id(self, student_id):
        """
        按学号精确查询学生
        
        Args:
            student_id: 学号
            
        Returns:
            Student: 学生对象
            
        Raises:
            StudentNotFoundError: 当学生不存在时
        """
        if not self._validate_student_id(student_id):
            logger.warning(f"无效的学号格式: {student_id}")
            raise StudentNotFoundError(student_id)
            
        student = self._students.get(student_id)
        if student:
            logger.debug(f"查询学生成功: 学号={student_id}, 姓名={student.name}")
            return student
        else:
            logger.debug(f"未找到学号为 {student_id} 的学生")
            raise StudentNotFoundError(student_id)
    
    def search_students_by_name(self, name):
        """
        按姓名模糊查询学生
        
        Args:
            name: 要搜索的姓名关键字
            
        Returns:
            list: 匹配的学生对象列表
        """
        logger.info(f"按姓名搜索: {name}")
        results = []
        
        # 空字符串不进行搜索
        if not name:
            logger.warning("搜索关键字不能为空")
            return results
            
        for student in self._students.values():
            if name.lower() in student.name.lower():
                results.append(student)
        
        logger.info(f"姓名搜索完成，找到 {len(results)} 名学生")
        return results
    
    def search_students_by_class(self, class_name):
        """
        按班级批量查询学生
        
        Args:
            class_name: 班级名称
            
        Returns:
            list: 该班级的所有学生对象列表
        """
        logger.info(f"按班级搜索: {class_name}")
        results = []
        
        # 空字符串不进行搜索
        if not class_name:
            logger.warning("班级名称不能为空")
            return results
            
        for student in self._students.values():
            if student.class_name == class_name:
                results.append(student)
        
        logger.info(f"班级搜索完成，找到 {len(results)} 名学生")
        return results
    
    def update_student(self, student_id, **kwargs):
        """
        更新学生信息
        
        Args:
            student_id: 学号
            **kwargs: 要更新的字段和值，支持name, gender, age, class_name, contact
            
        Returns:
            tuple: (是否成功, 消息)
            
        Raises:
            StudentNotFoundError: 当学生不存在时
            DataValidationError: 当数据验证失败时
            DataIOError: 当数据保存失败时
        """
        # 验证学号格式
        if not self._validate_student_id(student_id):
            error_msg = "学号格式不正确"
            logger.warning(f"更新学生失败 - {error_msg}")
            raise DataValidationError(error_msg)
        
        # 检查学生是否存在
        student = self.get_student_by_id(student_id)
        if not student:
            error_msg = f"学号 {student_id} 的学生不存在"
            logger.warning(f"更新学生失败 - {error_msg}")
            raise StudentNotFoundError(student_id)
        
        # 记录更新前的状态（用于日志）
        original_name = student.name
        
        try:
            # 定义可更新的字段列表
            allowed_fields = ['name', 'gender', 'age', 'class_name', 'contact']
            update_fields_info = {}
            has_changes = False
            
            # 执行更新
            updated_fields = []
            for field, value in kwargs.items():
                # 验证字段是否允许更新
                if field not in allowed_fields:
                    logger.warning(f"忽略未知字段: {field}")
                    continue
                
                # 跳过None值更新
                if value is None:
                    continue
                    
                # 对特殊字段进行验证和类型转换
                try:
                    if field == 'age':
                        value = int(value)
                        if value < 0 or value > 150:
                            raise DataValidationError("年龄必须在0-150之间")
                except ValueError:
                    raise DataValidationError("年龄必须是整数")
                    
                updated_fields.append(field)
                
            # 记录更新操作
            update_fields_str = ', '.join(updated_fields)
            logger.info(f"更新学生信息: 学号={student_id}, 姓名={original_name}, 更新字段={update_fields_str}")
            
            # 执行更新
            updated = student.update_info(**kwargs)
            
            # 如果有更新，则保存数据
            if updated:
                try:
                    if self._save_students():
                        success_msg = f"学生 {original_name} 信息更新成功"
                        logger.info(success_msg)
                        return True, success_msg
                    else:
                        # 如果保存失败，重新加载数据
                        self._load_students()
                        logger.error("保存数据失败，撤销更新操作")
                        raise DataIOError("保存数据失败", "更新学生信息", "保存")
                except Exception as save_error:
                    # 发生保存错误，重新加载数据以确保一致性
                    self._load_students()
                    logger.error(f"保存更新数据失败: {save_error}")
                    raise save_error
            else:
                logger.info(f"未对学生 {original_name} 进行任何更新")
                return False, "没有需要更新的信息"
                
        except DataValidationError:
            # 验证错误直接抛出
            raise
        except ValueError as e:
            logger.error(f"更新学生参数错误: {e}")
            raise DataValidationError(str(e))
        except Exception as e:
            logger.error(f"更新学生信息失败: {e}")
            raise OperationFailedError(f"更新学生信息失败: {str(e)}", operation="更新学生")
    
    def delete_student(self, student_id):
        """
        删除学生信息
        
        Args:
            student_id: 学号
            
        Returns:
            tuple: (是否成功, 消息)
            
        Raises:
            StudentNotFoundError: 当学生不存在时
            DataValidationError: 当数据验证失败时
            DataIOError: 当数据保存失败时
        """
        try:
            # 验证学号格式
            if not self._validate_student_id(student_id):
                error_msg = "学号格式不正确，无法执行删除操作"
                logger.warning(f"删除学生失败 - {error_msg}")
                raise DataValidationError(error_msg)
            
            # 检查学生是否存在
            if student_id not in self._students:
                logger.warning(f"删除学生失败 - 学号 {student_id} 不存在")
                raise StudentNotFoundError(student_id)
            
            # 获取学生信息用于日志
            student = self._students[student_id]
            student_name = student.name
            
            # 记录删除操作
            logger.info(f"删除学生: 学号={student_id}, 姓名={student_name}")
            
            # 从字典中删除学生
            del self._students[student_id]
            
            # 保存数据
            try:
                self._save_students()
                success_msg = f"学生 {student_name} 删除成功"
                logger.info(success_msg)
                return True, success_msg
            except Exception:
                # 如果保存失败，重新加载数据以确保一致性
                self._load_students()
                logger.error("保存数据失败，撤销删除操作")
                raise DataIOError("保存数据失败", "删除学生信息", "保存")
                
        except (StudentNotFoundError, DataValidationError, DataIOError):
            # 直接向上抛出这些特定异常
            raise
        except Exception as e:
            logger.error(f"删除学生失败: {e}")
            raise OperationFailedError(f"删除学生失败: {str(e)}", operation="删除学生")
    
    def delete_students_by_ids(self, student_ids):
        """
        批量删除学生信息
        
        Args:
            student_ids: 学号列表
            
        Returns:
            tuple: (成功删除的数量, 消息)
            
        Raises:
            DataValidationError: 当数据验证失败时
            DataIOError: 当数据保存失败时
        """
        deleted_count = 0
        not_found = []
        invalid_ids = []
        
        logger.info(f"批量删除学生操作，共 {len(student_ids)} 个学号")
        
        try:
            # 验证所有学号并检查存在性
            for student_id in student_ids:
                if not self._validate_student_id(student_id):
                    invalid_ids.append(student_id)
                elif student_id in self._students:
                    # 记录要删除的学生信息
                    student = self._students[student_id]
                    logger.debug(f"准备删除学生: 学号={student_id}, 姓名={student.name}")
                    deleted_count += 1
                else:
                    not_found.append(student_id)
            
            # 显示验证结果
            if invalid_ids:
                logger.warning(f"无效的学号格式: {', '.join(invalid_ids)}")
            if not_found:
                logger.warning(f"未找到的学号: {', '.join(not_found)}")
            
            # 如果没有有效学号可删除
            if deleted_count == 0:
                return 0, "没有找到可删除的学生"
            
            # 执行删除操作
            for student_id in [id for id in student_ids if self._validate_student_id(id) and id in self._students]:
                del self._students[student_id]
            
            # 保存数据
            try:
                if self._save_students():
                    message = f"成功删除 {deleted_count} 名学生"
                    if not_found:
                        message += f"。未找到的学号: {', '.join(not_found)}"
                    if invalid_ids:
                        message += f"。无效的学号格式: {', '.join(invalid_ids)}"
                    logger.info(message)
                    return deleted_count, message
                else:
                    # 如果保存失败，重新加载数据
                    self._load_students()
                    logger.error("保存数据失败，撤销批量删除操作")
                    raise DataIOError("保存数据失败", "批量删除", "保存")
            except Exception as save_error:
                # 发生保存错误，重新加载数据以确保一致性
                self._load_students()
                logger.error(f"保存批量删除后数据失败: {save_error}")
                raise save_error
                
        except (DataValidationError, DataIOError):
            raise
        except Exception as e:
            logger.error(f"批量删除学生失败: {e}")
            raise OperationFailedError(f"批量删除学生失败: {str(e)}")
    
    def delete_students_by_class(self, class_name):
        """
        按班级批量删除学生
        
        Args:
            class_name: 班级名称
            
        Returns:
            tuple: (成功删除的数量, 消息)
            
        Raises:
            DataValidationError: 当数据验证失败时
            DataIOError: 当数据保存失败时
        """
        # 验证班级名称不为空
        if not class_name:
            error_msg = "班级名称不能为空"
            logger.warning(f"按班级删除失败 - {error_msg}")
            raise DataValidationError(error_msg)
        
        logger.info(f"按班级删除学生操作: {class_name}")
        
        # 找出该班级的所有学生ID
        student_ids = []
        for student_id, student in self._students.items():
            if student.class_name == class_name:
                student_ids.append(student_id)
        
        if not student_ids:
            logger.info(f"班级 {class_name} 不存在或没有学生")
            return 0, f"班级 {class_name} 不存在或没有学生"
        
        logger.info(f"找到班级 {class_name} 的 {len(student_ids)} 名学生")
        
        # 调用批量删除方法
        try:
            return self.delete_students_by_ids(student_ids)
        except Exception as e:
            logger.error(f"按班级删除学生失败: {e}")
            raise OperationFailedError(f"按班级删除学生失败: {str(e)}")
    
    def get_all_students(self):
        """
        获取所有学生信息
        
        Returns:
            list: 所有学生对象列表
        """
        logger.info(f"获取所有学生信息，共 {len(self._students)} 名学生")
        return list(self._students.values())
    
    def get_student_count(self):
        """
        获取学生总数
        
        Returns:
            int: 学生数量
        """
        count = len(self._students)
        logger.debug(f"当前学生总数: {count}")
        return count
    
    def get_class_list(self):
        """
        获取所有班级列表
        
        Returns:
            list: 不重复的班级名称列表
        """
        class_set = set()
        for student in self._students.values():
            class_set.add(student.class_name)
        
        class_list = sorted(list(class_set))
        logger.info(f"获取班级列表，共 {len(class_list)} 个班级")
        
        return class_list
    
    def get_class_student_count(self, class_name):
        """
        获取指定班级的学生数量
        
        Args:
            class_name: 班级名称
            
        Returns:
            int: 学生数量
        """
        # 验证班级名称不为空
        if not class_name:
            logger.warning("班级名称不能为空")
            return 0
            
        count = 0
        for student in self._students.values():
            if student.class_name == class_name:
                count += 1
        
        logger.info(f"班级 {class_name} 的学生数量: {count}")
        return count
    
    def backup_data(self):
        """
        备份数据
        
        Returns:
            str: 备份文件路径
            
        Raises:
            BackupRestoreError: 当备份失败时
        """
        try:
            logger.info("执行数据备份操作")
            backup_path = self._data_manager.backup_data()
            logger.info(f"数据备份成功: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"数据备份失败: {e}")
            raise OperationFailedError(f"数据备份失败: {str(e)}")
    
    def _validate_student_id(self, student_id):
        """
        验证学号格式
        学号可以包含字母、数字和下划线，长度在3-20个字符之间
        
        Args:
            student_id: 学号
            
        Returns:
            bool: 格式是否正确
        """
        if not isinstance(student_id, str):
            return False
        
        # 使用正则表达式验证
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        result = bool(re.match(pattern, student_id))
        
        if not result:
            logger.debug(f"无效的学号格式: {student_id}")
            
        return result
        
    def import_data(self, import_file, overwrite=False):
        """
        导入学生数据
        
        Args:
            import_file: 导入文件路径
            overwrite: 是否覆盖现有数据
            
        Returns:
            dict: 导入的学生数据
            
        Raises:
            DataIOError: 当导入失败时
            EmptyDataError: 当文件不存在或为空时
        """
        try:
            logger.info(f"导入学生数据: 文件={import_file}, 覆盖模式={overwrite}")
            imported_data = self._data_manager.import_data(import_file, overwrite)
            
            # 重新加载数据以确保内存与文件一致
            self._load_students()
            
            logger.info(f"数据导入成功，共导入 {len(imported_data)} 名学生")
            return imported_data
        except Exception as e:
            logger.error(f"导入学生数据失败: {e}")
            # 重新加载数据以确保一致性
            self._load_students()
            raise
            
    def export_data(self, export_file):
        """
        导出学生数据
        
        Args:
            export_file: 导出文件路径
            
        Returns:
            bool: 导出是否成功
            
        Raises:
            DataIOError: 当导出失败时
        """
        try:
            logger.info(f"导出学生数据到文件: {export_file}")
            success = self._data_manager.export_data(export_file)
            logger.info(f"学生数据导出{'成功' if success else '失败'}")
            return success
        except Exception as e:
            logger.error(f"导出学生数据失败: {e}")
            raise
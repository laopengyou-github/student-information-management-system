import os
import time
from datetime import datetime
from src.utils.logger import logger
from src.utils.exceptions import (
    StudentNotFoundError,
    StudentAlreadyExistsError as StudentExistsError,
    DataValidationError,
    OperationFailedError,
    DataIOError,
    handle_exception
)

class UserInterface:
    """
    用户界面类，提供命令行交互界面
    实现菜单显示、用户输入处理和结果展示等功能
    集成了异常处理和日志记录功能
    """
    
    def __init__(self, student_manager):
        """
        初始化用户界面
        
        Args:
            student_manager: 学生管理器实例
        """
        logger.info("初始化用户界面")
        self._student_manager = student_manager
        logger.info("用户界面初始化完成")
    
    def clear_screen(self):
        """
        清屏函数，根据不同操作系统使用不同命令
        """
        # Windows 使用 'cls'，其他系统使用 'clear'
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self, message="按回车键继续..."):
        """
        暂停函数，等待用户输入
        
        Args:
            message: 显示的提示信息
        """
        input(message)
    
    def print_title(self, title):
        """
        打印带边框的标题
        
        Args:
            title: 标题文本
        """
        self.clear_screen()
        print("=" * 60)
        print(f"{' ' * 20}{title}{' ' * 20}")
        print("=" * 60)
    
    def print_menu(self, menu_items):
        """
        打印菜单选项
        
        Args:
            menu_items: 菜单项列表，每个元素是(选项号, 选项描述)的元组
        """
        print("\n请选择操作：")
        for item in menu_items:
            print(f"  {item[0]}. {item[1]}")
        print()
    
    def get_input(self, prompt, required=True, default=None, input_type=str):
        """
        获取用户输入，并进行基本验证
        
        Args:
            prompt: 提示信息
            required: 是否为必填项
            default: 默认值
            input_type: 输入类型转换
            
        Returns:
            转换后的输入值或默认值
        """
        while True:
            try:
                if default is not None:
                    user_input = input(f"{prompt} [{default}]: ")
                    if not user_input.strip():
                        return default
                else:
                    user_input = input(f"{prompt}: ")
                
                # 如果是必填项但用户未输入
                if required and not user_input.strip():
                    print("该项为必填项，请重新输入")
                    continue
                
                # 如果不是必填项且用户未输入，返回空字符串
                if not required and not user_input.strip():
                    return ""
                
                # 尝试类型转换
                return input_type(user_input)
                
            except ValueError:
                print(f"输入类型错误，请输入{input_type.__name__}类型的值")
            except Exception as e:
                logger.error(f"获取用户输入时发生错误: {e}")
                print(f"发生错误: {str(e)}")
    
    def print_student_info(self, student):
        """
        格式化打印单个学生信息
        
        Args:
            student: 学生对象
        """
        print("\n" + "-" * 60)
        print(f"学号: {student.student_id}")
        print(f"姓名: {student.name}")
        print(f"性别: {student.gender}")
        print(f"年龄: {student.age}")
        print(f"班级: {student.class_name}")
        print(f"联系方式: {student.contact}")
        print("-" * 60)
    
    def print_student_table(self, students):
        """
        表格形式打印学生列表
        
        Args:
            students: 学生对象列表
        """
        if not students:
            print("\n没有找到符合条件的学生")
            return
        
        # 打印表头
        print("\n" + "-" * 80)
        print(f"{'学号':<15} {'姓名':<10} {'性别':<5} {'年龄':<5} {'班级':<15} {'联系方式':<20}")
        print("-" * 80)
        
        # 打印学生信息
        for student in students:
            print(f"{student.student_id:<15} {student.name:<10} {student.gender:<5} "
                  f"{student.age:<5} {student.class_name:<15} {student.contact:<20}")
        
        print("-" * 80)
        print(f"\n共找到 {len(students)} 名学生")
    
    def show_main_menu(self):
        """
        显示主菜单
        """
        while True:
            self.print_title("学生信息管理系统")
            print(f"当前系统时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"系统中的学生总数: {self._student_manager.get_student_count()}")
            
            menu_items = [
                ("1", "添加学生信息"),
                ("2", "查询学生信息"),
                ("3", "修改学生信息"),
                ("4", "删除学生信息"),
                ("5", "显示所有学生"),
                ("6", "系统统计信息"),
                ("7", "数据备份与恢复"),
                ("0", "退出系统")
            ]
            
            self.print_menu(menu_items)
            choice = input("请输入您的选择 [0-7]: ")
            
            if choice == "1":
                self.add_student_menu()
            elif choice == "2":
                self.search_student_menu()
            elif choice == "3":
                self.update_student_menu()
            elif choice == "4":
                self.delete_student_menu()
            elif choice == "5":
                self.show_all_students()
            elif choice == "6":
                self.show_statistics()
            elif choice == "7":
                self.data_backup_menu()
            elif choice == "0":
                if self.confirm_exit():
                    self.print_title("感谢使用学生信息管理系统")
                    print("\n再见！")
                    time.sleep(1)
                    break
            else:
                print("无效的选择，请重新输入")
                self.pause()
    
    def add_student_menu(self):
        """
        添加学生菜单
        """
        self.print_title("添加学生信息")
        
        try:
            # 获取学生信息
            student_id = self.get_input("请输入学号")
            name = self.get_input("请输入姓名")
            
            # 性别输入验证
            while True:
                gender = self.get_input("请输入性别 (男/女)")
                if gender in ['男', '女']:
                    break
                else:
                    print("性别必须为'男'或'女'，请重新输入")
            
            age = self.get_input("请输入年龄", input_type=int)
            class_name = self.get_input("请输入班级")
            contact = self.get_input("请输入联系方式")
            
            # 确认添加
            print("\n请确认学生信息：")
            print(f"学号: {student_id}, 姓名: {name}, 性别: {gender}, 年龄: {age}, 班级: {class_name}, 联系方式: {contact}")
            
            confirm = self.get_input("确认添加？(y/n)", required=False, default="y").lower()
            if confirm == 'y':
                # 调用添加方法
                try:
                    success, message = self._student_manager.add_student(
                        student_id, name, gender, age, class_name, contact
                    )
                    print(f"\n{message}")
                    if success:
                        self.log_operation(f"添加学生: {name} (学号: {student_id})")
                except StudentExistsError as e:
                    print(f"\n操作失败: 学号已存在")
                    logger.warning(f"添加学生失败: {e}")
                except DataValidationError as e:
                    print(f"\n操作失败: {str(e)}")
                    logger.warning(f"添加学生失败: {e}")
                except DataIOError as e:
                    print(f"\n操作失败: 数据保存失败，请稍后重试")
                    logger.error(f"添加学生失败: {e}")
                except OperationFailedError as e:
                    print(f"\n操作失败: {str(e)}")
                    logger.error(f"添加学生失败: {e}")
                except Exception as e:
                    print(f"\n操作失败: 发生未知错误")
                    logger.error(f"添加学生时发生未知错误: {e}")
            else:
                print("\n已取消添加")
        except KeyboardInterrupt:
            print("\n\n操作已取消")
        except Exception as e:
            handle_exception(e, "添加学生菜单")
        
        self.pause()
    
    def search_student_menu(self):
        """
        查询学生菜单
        """
        try:
            while True:
                self.print_title("查询学生信息")
                
                search_menu = [
                    ("1", "按学号精确查询"),
                    ("2", "按姓名模糊查询"),
                    ("3", "按班级查询"),
                    ("0", "返回主菜单")
                ]
                
                self.print_menu(search_menu)
                choice = input("请选择查询方式 [0-3]: ")
                
                try:
                    if choice == "1":
                        student_id = self.get_input("请输入学号")
                        student = self._student_manager.get_student_by_id(student_id)
                        if student:
                            self.print_student_info(student)
                            self.log_operation(f"查询学生: {student.name} (学号: {student_id})")
                        else:
                            print(f"\n未找到学号为 {student_id} 的学生")
                        self.pause()
                        
                    elif choice == "2":
                        name = self.get_input("请输入姓名关键字")
                        students = self._student_manager.search_students_by_name(name)
                        self.print_student_table(students)
                        self.log_operation(f"按姓名查询: {name}")
                        self.pause()
                        
                    elif choice == "3":
                        class_name = self.get_input("请输入班级名称")
                        students = self._student_manager.search_students_by_class(class_name)
                        self.print_student_table(students)
                        self.log_operation(f"按班级查询: {class_name}")
                        self.pause()
                        
                    elif choice == "0":
                        break
                    else:
                        print("无效的选择，请重新输入")
                        self.pause()
                except Exception as e:
                    print(f"\n查询过程中发生错误: {str(e)}")
                    logger.error(f"查询学生失败: {e}")
                    self.pause()
        except KeyboardInterrupt:
            print("\n\n操作已取消")
        except Exception as e:
            handle_exception(e, "查询学生菜单")
    
    def update_student_menu(self):
        """
        修改学生菜单
        """
        self.print_title("修改学生信息")
        
        try:
            student_id = self.get_input("请输入要修改的学生学号")
            student = self._student_manager.get_student_by_id(student_id)
            
            if not student:
                print(f"\n未找到学号为 {student_id} 的学生")
                self.pause()
                return
            
            # 显示当前信息
            self.print_student_info(student)
            print("\n请输入新的信息（回车保留原值）：")
            
            # 获取新值，允许保留原值
            name = self.get_input("请输入姓名", required=False)
            gender = self.get_input("请输入性别 (男/女)", required=False)
            age_str = self.get_input("请输入年龄", required=False)
            class_name = self.get_input("请输入班级", required=False)
            contact = self.get_input("请输入联系方式", required=False)
            
            # 构建更新参数
            update_data = {}
            if name:
                update_data['name'] = name
            if gender:
                if gender in ['男', '女']:
                    update_data['gender'] = gender
                else:
                    print("性别必须为'男'或'女'，跳过更新该字段")
            if age_str:
                try:
                    update_data['age'] = int(age_str)
                except ValueError:
                    print("年龄必须为整数，跳过更新该字段")
            if class_name:
                update_data['class_name'] = class_name
            if contact:
                update_data['contact'] = contact
            
            # 执行更新
            if update_data:
                try:
                    success, message = self._student_manager.update_student(student_id, **update_data)
                    print(f"\n{message}")
                    if success:
                        self.log_operation(f"修改学生: {student.name} (学号: {student_id})")
                except StudentNotFoundError as e:
                    print(f"\n操作失败: 学生不存在")
                    logger.warning(f"修改学生失败: {e}")
                except DataValidationError as e:
                    print(f"\n操作失败: {str(e)}")
                    logger.warning(f"修改学生失败: {e}")
                except DataIOError as e:
                    print(f"\n操作失败: 数据保存失败，请稍后重试")
                    logger.error(f"修改学生失败: {e}")
                except OperationFailedError as e:
                    print(f"\n操作失败: {str(e)}")
                    logger.error(f"修改学生失败: {e}")
                except Exception as e:
                    print(f"\n操作失败: 发生未知错误")
                    logger.error(f"修改学生时发生未知错误: {e}")
            else:
                print("\n未修改任何信息")
        except KeyboardInterrupt:
            print("\n\n操作已取消")
        except Exception as e:
            handle_exception(e, "修改学生菜单")
        
        self.pause()
    
    def delete_student_menu(self):
        """
        删除学生菜单
        """
        try:
            while True:
                self.print_title("删除学生信息")
                
                delete_menu = [
                    ("1", "按学号单个删除"),
                    ("2", "按学号批量删除"),
                    ("3", "按班级批量删除"),
                    ("0", "返回主菜单")
                ]
                
                self.print_menu(delete_menu)
                choice = input("请选择删除方式 [0-3]: ")
                
                try:
                    if choice == "1":
                        student_id = self.get_input("请输入要删除的学生学号")
                        student = self._student_manager.get_student_by_id(student_id)
                        
                        if not student:
                            print(f"\n未找到学号为 {student_id} 的学生")
                        else:
                            self.print_student_info(student)
                            confirm = self.get_input(f"确认删除学生 {student.name}？(y/n)", 
                                                    required=False, default="n").lower()
                            
                            if confirm == 'y':
                                try:
                                    success, message = self._student_manager.delete_student(student_id)
                                    print(f"\n{message}")
                                    if success:
                                        self.log_operation(f"删除学生: {student.name} (学号: {student_id})")
                                except StudentNotFoundError as e:
                                    print(f"\n操作失败: 学生不存在")
                                    logger.warning(f"删除学生失败: {e}")
                                except DataValidationError as e:
                                    print(f"\n操作失败: {str(e)}")
                                    logger.warning(f"删除学生失败: {e}")
                                except DataIOError as e:
                                    print(f"\n操作失败: 数据保存失败，请稍后重试")
                                    logger.error(f"删除学生失败: {e}")
                                except OperationFailedError as e:
                                    print(f"\n操作失败: {str(e)}")
                                    logger.error(f"删除学生失败: {e}")
                                except Exception as e:
                                    print(f"\n操作失败: 发生未知错误")
                                    logger.error(f"删除学生时发生未知错误: {e}")
                            else:
                                print("\n已取消删除")
                        
                        self.pause()
                        
                    elif choice == "2":
                        student_ids_str = self.get_input("请输入要删除的学生学号（多个学号用逗号分隔）")
                        student_ids = [s.strip() for s in student_ids_str.split(',') if s.strip()]
                        
                        if not student_ids:
                            print("\n没有输入有效的学号")
                        else:
                            # 显示要删除的学生信息
                            print("\n即将删除的学生：")
                            found_students = []
                            for student_id in student_ids:
                                student = self._student_manager.get_student_by_id(student_id)
                                if student:
                                    found_students.append(student)
                                    print(f"- {student.name} (学号: {student_id})")
                            
                            if found_students:
                                confirm = self.get_input(f"确认删除这 {len(found_students)} 名学生？(y/n)", 
                                                        required=False, default="n").lower()
                                
                                if confirm == 'y':
                                    try:
                                        count, message = self._student_manager.delete_students_by_ids(student_ids)
                                        print(f"\n{message}")
                                        if count > 0:
                                            self.log_operation(f"批量删除学生: 共{count}名")
                                    except DataValidationError as e:
                                        print(f"\n操作失败: {str(e)}")
                                        logger.warning(f"批量删除学生失败: {e}")
                                    except DataIOError as e:
                                        print(f"\n操作失败: 数据保存失败，请稍后重试")
                                        logger.error(f"批量删除学生失败: {e}")
                                    except OperationFailedError as e:
                                        print(f"\n操作失败: {str(e)}")
                                        logger.error(f"批量删除学生失败: {e}")
                                    except Exception as e:
                                        print(f"\n操作失败: 发生未知错误")
                                        logger.error(f"批量删除学生时发生未知错误: {e}")
                            else:
                                print("\n未找到任何要删除的学生")
                        
                        self.pause()
                        
                    elif choice == "3":
                        class_name = self.get_input("请输入要删除的班级名称")
                        students = self._student_manager.search_students_by_class(class_name)
                        
                        if not students:
                            print(f"\n班级 {class_name} 不存在或没有学生")
                        else:
                            print(f"\n班级 {class_name} 共有 {len(students)} 名学生：")
                            self.print_student_table(students)
                            
                            confirm = self.get_input(f"确认删除班级 {class_name} 的所有 {len(students)} 名学生？(y/n)", 
                                                    required=False, default="n").lower()
                            
                            if confirm == 'y':
                                try:
                                    count, message = self._student_manager.delete_students_by_class(class_name)
                                    print(f"\n{message}")
                                    if count > 0:
                                        self.log_operation(f"按班级删除学生: {class_name} 共{count}名")
                                except DataValidationError as e:
                                    print(f"\n操作失败: {str(e)}")
                                    logger.warning(f"按班级删除学生失败: {e}")
                                except DataIOError as e:
                                    print(f"\n操作失败: 数据保存失败，请稍后重试")
                                    logger.error(f"按班级删除学生失败: {e}")
                                except OperationFailedError as e:
                                    print(f"\n操作失败: {str(e)}")
                                    logger.error(f"按班级删除学生失败: {e}")
                                except Exception as e:
                                    print(f"\n操作失败: 发生未知错误")
                                    logger.error(f"按班级删除学生时发生未知错误: {e}")
                        
                        self.pause()
                        
                    elif choice == "0":
                        break
                    else:
                        print("无效的选择，请重新输入")
                        self.pause()
                except Exception as e:
                    print(f"\n删除过程中发生错误: {str(e)}")
                    logger.error(f"删除学生失败: {e}")
                    self.pause()
        except KeyboardInterrupt:
            print("\n\n操作已取消")
        except Exception as e:
            handle_exception(e, "删除学生菜单")
    
    def show_all_students(self):
        """
        显示所有学生信息
        """
        try:
            self.print_title("所有学生信息")
            students = self._student_manager.get_all_students()
            self.print_student_table(students)
            self.log_operation("查看所有学生信息")
        except Exception as e:
            print(f"\n获取学生信息时发生错误: {str(e)}")
            logger.error(f"查看所有学生信息失败: {e}")
        
        self.pause()
    
    def show_statistics(self):
        """
        显示系统统计信息
        """
        try:
            self.print_title("系统统计信息")
            
            total_students = self._student_manager.get_student_count()
            print(f"\n学生总数: {total_students}")
            
            class_list = self._student_manager.get_class_list()
            print(f"\n班级数量: {len(class_list)}")
            
            if class_list:
                print("\n各班级学生数量：")
                for class_name in class_list:
                    count = self._student_manager.get_class_student_count(class_name)
                    print(f"  {class_name}: {count} 名")
            
            # 计算年龄统计（如果有学生）
            if total_students > 0:
                students = self._student_manager.get_all_students()
                ages = [s.age for s in students]
                avg_age = sum(ages) / len(ages)
                max_age = max(ages)
                min_age = min(ages)
                
                print(f"\n年龄统计：")
                print(f"  平均年龄: {avg_age:.1f}")
                print(f"  最大年龄: {max_age}")
                print(f"  最小年龄: {min_age}")
            
            self.log_operation("查看系统统计信息")
        except Exception as e:
            print(f"\n获取统计信息时发生错误: {str(e)}")
            logger.error(f"查看系统统计信息失败: {e}")
        
        self.pause()
    
    def data_backup_menu(self):
        """
        数据备份与恢复菜单
        """
        try:
            while True:
                self.print_title("数据备份与恢复")
                
                backup_menu = [
                    ("1", "备份当前数据"),
                    ("2", "导入数据"),
                    ("3", "导出数据"),
                    ("0", "返回主菜单")
                ]
                
                self.print_menu(backup_menu)
                choice = input("请选择操作 [0-3]: ")
                
                try:
                    if choice == "1":
                        try:
                            backup_file = self._student_manager.backup_data()
                            print(f"\n数据备份成功！")
                            print(f"备份文件路径: {backup_file}")
                            self.log_operation(f"数据备份成功: {backup_file}")
                        except OperationFailedError as e:
                            print(f"\n数据备份失败: {str(e)}")
                            logger.error(f"数据备份失败: {e}")
                        except Exception as e:
                            print(f"\n数据备份失败: 发生未知错误")
                            logger.error(f"数据备份时发生未知错误: {e}")
                        self.pause()
                    
                    elif choice == "2":
                        self.import_data_menu()
                    
                    elif choice == "3":
                        self.export_data_menu()
                    
                    elif choice == "0":
                        break
                    else:
                        print("无效的选择，请重新输入")
                        self.pause()
                except Exception as e:
                    print(f"\n操作过程中发生错误: {str(e)}")
                    logger.error(f"数据备份菜单操作失败: {e}")
                    self.pause()
        except KeyboardInterrupt:
            print("\n\n操作已取消")
        except Exception as e:
            handle_exception(e, "数据备份菜单")
    
    def import_data_menu(self):
        """
        导入数据菜单
        """
        self.print_title("导入数据")
        
        try:
            import_file = self.get_input("请输入导入文件路径")
            
            # 检查文件是否存在
            if not os.path.exists(import_file):
                print(f"\n文件 {import_file} 不存在")
                self.pause()
                return
            
            # 询问是否覆盖
            confirm = self.get_input("是否覆盖现有数据？(y/n)", 
                                   required=False, default="n").lower()
            overwrite = confirm == 'y'
            
            print("\n开始导入数据...")
            
            try:
                imported_data = self._student_manager.import_data(import_file, overwrite)
                print(f"\n数据导入成功！")
                print(f"导入了 {len(imported_data)} 条学生记录")
                self.log_operation(f"导入数据成功: {import_file}")
            except DataIOError as e:
                print(f"\n数据导入失败: {str(e)}")
                logger.error(f"导入数据失败: {e}")
            except Exception as e:
                print(f"\n数据导入失败: 发生未知错误")
                logger.error(f"导入数据时发生未知错误: {e}")
        except KeyboardInterrupt:
            print("\n\n操作已取消")
        except Exception as e:
            print(f"\n导入数据时发生错误: {str(e)}")
            logger.error(f"导入数据菜单失败: {e}")
        
        self.pause()
    
    def export_data_menu(self):
        """
        导出数据菜单
        """
        self.print_title("导出数据")
        
        try:
            export_file = self.get_input("请输入导出文件路径")
            
            # 检查文件是否已存在
            if os.path.exists(export_file):
                confirm = self.get_input("文件已存在，是否覆盖？(y/n)", 
                                       required=False, default="n").lower()
                if confirm != 'y':
                    print("\n已取消导出")
                    self.pause()
                    return
            
            print("\n开始导出数据...")
            
            try:
                success = self._student_manager.export_data(export_file)
                if success:
                    print(f"\n数据导出成功！")
                    print(f"导出文件路径: {export_file}")
                    self.log_operation(f"导出数据成功: {export_file}")
                else:
                    print("\n数据导出失败")
            except DataIOError as e:
                print(f"\n数据导出失败: {str(e)}")
                logger.error(f"导出数据失败: {e}")
            except Exception as e:
                print(f"\n数据导出失败: 发生未知错误")
                logger.error(f"导出数据时发生未知错误: {e}")
        except KeyboardInterrupt:
            print("\n\n操作已取消")
        except Exception as e:
            print(f"\n导出数据时发生错误: {str(e)}")
            logger.error(f"导出数据菜单失败: {e}")
        
        self.pause()
    
    def confirm_exit(self):
        """
        确认退出
        
        Returns:
            bool: 是否确认退出
        """
        try:
            confirm = input("\n确定要退出系统吗？(y/n): ").lower()
            if confirm == 'y':
                self.log_operation("退出系统")
                logger.info("用户确认退出系统")
            return confirm == 'y'
        except Exception as e:
            logger.error(f"确认退出时发生错误: {e}")
            return False
    
    def log_operation(self, operation):
        """
        记录操作日志
        集成到完整的日志系统中
        
        Args:
            operation: 操作描述
        """
        try:
            # 使用日志模块记录操作
            logger.info(f"用户操作: {operation}")
        except Exception as e:
            # 避免日志记录失败影响主程序
            print(f"记录日志失败: {str(e)}")
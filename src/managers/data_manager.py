import json
import os
import shutil
from datetime import datetime
from src.utils.logger import logger
from src.utils.exceptions import (
    DataIOError,
    BackupRestoreError,
    EmptyDataError,
    SystemConfigError
)

class DataManager:
    """
    数据管理模块，负责学生数据的持久化存储和读取
    使用JSON格式存储数据
    集成了异常处理和日志记录功能
    """
    
    def __init__(self, data_file="data/students.json"):
        """
        初始化数据管理器
        
        Args:
            data_file: 数据文件路径，默认为"data/students.json"
            
        Raises:
            SystemConfigError: 当配置无效时
        """
        # 验证配置
        if not data_file:
            raise SystemConfigError("数据文件路径不能为空", "data_config")
        
        self._data_file = data_file
        # 记录初始化信息
        logger.info(f"初始化数据管理器: 数据文件={data_file}")
        # 确保数据目录存在
        try:
            self._ensure_data_dir_exists()
            logger.debug("数据目录创建/验证成功")
        except Exception as e:
            logger.error(f"创建目录失败: {e}")
            raise SystemConfigError(f"无法创建必要的目录: {e}", "directory_creation")
    
    def _ensure_data_dir_exists(self):
        """
        确保数据目录存在，如果不存在则创建
        """
        data_dir = os.path.dirname(self._data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_data(self, students_data):
        """
        将学生数据保存到JSON文件中
        
        Args:
            students_data: 学生数据字典，格式为{student_id: student_dict}
            
        Returns:
            bool: 保存是否成功
            
        Raises:
            DataIOError: 当数据保存失败时
        """
        try:
            logger.info(f"开始保存数据到文件: {self._data_file}")
            logger.debug(f"保存数据大小: {len(students_data)} 条记录")
            
            # 将学生数据保存到JSON文件
            with open(self._data_file, 'w', encoding='utf-8') as f:
                json.dump(students_data, f, ensure_ascii=False, indent=4)
            
            logger.info(f"数据保存成功")
            return True
        except Exception as e:
            error_msg = f"保存数据失败: {str(e)}"
            logger.error(error_msg)
            raise DataIOError(str(e), self._data_file, "保存")
    
    def load_data(self):
        """
        从JSON文件中加载学生数据
        
        Returns:
            dict: 学生数据字典，如果文件不存在或加载失败则返回空字典
            
        Raises:
            DataIOError: 当数据加载失败时
        """
        try:
            logger.info(f"开始加载数据从文件: {self._data_file}")
            
            if not os.path.exists(self._data_file):
                # 如果文件不存在，返回空字典
                logger.warning(f"数据文件不存在: {self._data_file}，返回空数据")
                return {}
            
            with open(self._data_file, 'r', encoding='utf-8') as f:
                students_data = json.load(f)
            
            logger.info(f"数据加载成功，共 {len(students_data)} 条记录")
            return students_data
        except json.JSONDecodeError as e:
            error_msg = f"数据文件格式错误: {str(e)}"
            logger.error(error_msg)
            raise DataIOError(f"JSON解析错误: {str(e)}", self._data_file, "读取")
        except Exception as e:
            error_msg = f"加载数据失败: {str(e)}"
            logger.error(error_msg)
            raise DataIOError(str(e), self._data_file, "读取")
    
    def backup_data(self, backup_dir="data/backups"):
        """
        备份当前数据文件
        
        Args:
            backup_dir: 备份目录
            
        Returns:
            str: 备份文件路径
            
        Raises:
            BackupRestoreError: 当备份创建失败时
            EmptyDataError: 当没有数据可备份时
        """
        try:
            logger.info("开始创建数据备份")
            
            # 确保备份目录存在
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                logger.debug(f"创建备份目录: {backup_dir}")
            
            # 检查原数据文件是否存在
            if not os.path.exists(self._data_file):
                logger.warning("源数据文件不存在，无法备份")
                raise EmptyDataError("没有数据文件可供备份")
            
            # 检查文件大小，确保有数据
            if os.path.getsize(self._data_file) == 0:
                logger.warning("数据文件为空，无法备份")
                raise EmptyDataError("数据文件为空，无法备份")
            
            # 生成备份文件名，包含时间戳
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"students_backup_{timestamp}.json"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # 复制文件进行备份
            shutil.copy2(self._data_file, backup_path)
            
            logger.info(f"备份创建成功: {backup_path}")
            return backup_path
        except EmptyDataError:
            raise
        except Exception as e:
            error_msg = f"创建备份失败: {str(e)}"
            logger.error(error_msg)
            raise BackupRestoreError(str(e), "备份")
    
    def restore_data(self, backup_file):
        """
        从备份文件恢复数据
        
        Args:
            backup_file: 备份文件路径
            
        Returns:
            bool: 恢复是否成功
            
        Raises:
            BackupRestoreError: 当恢复失败时
            EmptyDataError: 当备份文件不存在或为空时
        """
        try:
            logger.info(f"开始从备份恢复数据: {backup_file}")
            
            if not os.path.exists(backup_file):
                logger.error(f"备份文件不存在: {backup_file}")
                raise EmptyDataError(f"备份文件不存在: {backup_file}")
            
            # 验证备份文件是否有效
            if os.path.getsize(backup_file) == 0:
                logger.error(f"备份文件为空: {backup_file}")
                raise EmptyDataError(f"备份文件为空: {backup_file}")
            
            # 先备份当前数据
            pre_restore_backup = self.backup_data()
            logger.info(f"恢复前创建了当前数据的备份: {pre_restore_backup}")
            
            # 复制备份文件到数据文件位置
            shutil.copy2(backup_file, self._data_file)
            
            logger.info(f"数据恢复成功")
            return True
        except (BackupRestoreError, EmptyDataError):
            raise
        except Exception as e:
            error_msg = f"恢复备份失败: {str(e)}"
            logger.error(error_msg)
            raise BackupRestoreError(str(e), "恢复")
    
    def export_data(self, export_file, format="json"):
        """
        导出数据到指定格式的文件
        
        Args:
            export_file: 导出文件路径
            format: 导出格式，当前仅支持json
            
        Returns:
            bool: 导出是否成功
            
        Raises:
            DataIOError: 当导出失败时
            InvalidOperationError: 当格式不支持时
        """
        try:
            logger.info(f"开始导出数据到: {export_file}, 格式: {format}")
            
            if format.lower() == "json":
                # 加载当前数据
                students_data = self.load_data()
                logger.debug(f"导出数据大小: {len(students_data)} 条记录")
                
                # 确保输出目录存在
                os.makedirs(os.path.dirname(export_file), exist_ok=True)
                
                # 导出为JSON文件
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(students_data, f, ensure_ascii=False, indent=4)
                
                logger.info(f"数据导出成功")
                return True
            else:
                from src.utils.exceptions import InvalidOperationError
                logger.error(f"不支持的导出格式: {format}")
                raise InvalidOperationError(f"不支持的导出格式: {format}")
        except InvalidOperationError:
            raise
        except Exception as e:
            error_msg = f"导出数据失败: {str(e)}"
            logger.error(error_msg)
            raise DataIOError(str(e), export_file, "导出")
    
    def import_data(self, import_file, overwrite=False):
        """
        从外部文件导入数据
        
        Args:
            import_file: 导入文件路径
            overwrite: 是否覆盖现有数据，如果为False则合并数据
            
        Returns:
            dict: 导入的学生数据字典
            
        Raises:
            DataIOError: 当导入失败时
            EmptyDataError: 当输入文件不存在时
        """
        try:
            logger.info(f"开始从文件导入数据: {import_file}, 覆盖模式: {overwrite}")
            
            if not os.path.exists(import_file):
                logger.error(f"导入文件不存在: {import_file}")
                raise EmptyDataError(f"导入文件不存在: {import_file}")
            
            # 验证文件大小
            if os.path.getsize(import_file) == 0:
                logger.error(f"导入文件为空: {import_file}")
                raise EmptyDataError(f"导入文件为空: {import_file}")
            
            # 加载导入文件数据
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            if not isinstance(imported_data, dict):
                raise DataIOError("导入数据格式错误，必须是字典格式", import_file, "导入")
            
            if overwrite:
                # 覆盖现有数据
                logger.info(f"覆盖现有数据，导入 {len(imported_data)} 条记录")
                self.save_data(imported_data)
            else:
                # 合并数据
                current_data = self.load_data()
                current_count = len(current_data)
                current_data.update(imported_data)
                new_count = len(current_data)
                added_count = new_count - current_count
                logger.info(f"合并数据，新增 {added_count} 条记录，总计 {new_count} 条记录")
                self.save_data(current_data)
            
            return imported_data
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"导入文件格式错误: {import_file}, 错误: {str(e)}")
            raise DataIOError(f"JSON解析错误: {str(e)}", import_file, "导入")
        except (DataIOError, EmptyDataError):
            raise
        except Exception as e:
            logger.error(f"导入数据失败: {str(e)}")
            raise DataIOError(str(e), import_file, "导入")
    
    def get_data_file_info(self):
        """
        获取数据文件信息
        
        Returns:
            dict: 包含数据文件路径、大小、修改时间等信息的字典
        """
        try:
            logger.info(f"获取数据文件信息: {self._data_file}")
            
            info = {
                "file_path": self._data_file,
                "exists": os.path.exists(self._data_file),
                "size": 0,
                "last_modified": None
            }
            
            if info["exists"]:
                info["size"] = os.path.getsize(self._data_file)
                last_modified_timestamp = os.path.getmtime(self._data_file)
                info["last_modified"] = datetime.fromtimestamp(last_modified_timestamp).strftime("%Y-%m-%d %H:%M:%S")
                logger.debug(f"文件信息: {info}")
            else:
                logger.debug("数据文件不存在")
            
            return info
        except Exception as e:
            logger.error(f"获取文件信息失败: {e}")
            # 出错时返回默认信息
            return {
                "file_path": self._data_file,
                "exists": False,
                "size": 0,
                "last_modified": None
            }
    
    def clear_data(self):
        """
        清空所有数据
        
        Returns:
            bool: 清空是否成功
            
        Raises:
            DataIOError: 当删除失败时
        """
        try:
            logger.warning(f"开始清空所有数据: {self._data_file}")
            
            # 在删除前先创建备份
            if os.path.exists(self._data_file):
                try:
                    backup_path = self.backup_data()
                    logger.info(f"删除前创建了备份: {backup_path}")
                except Exception as backup_error:
                    logger.warning(f"创建备份失败，但继续删除数据: {backup_error}")
                
                os.remove(self._data_file)
                logger.warning(f"数据文件已删除")
            else:
                logger.warning("数据文件不存在，无需删除")
            
            return True
        except Exception as e:
            error_msg = f"清空数据失败: {str(e)}"
            logger.error(error_msg)
            raise DataIOError(str(e), self._data_file, "删除")
    
    def cleanup_old_backups(self, backup_dir="data/backups", keep_days=30):
        """
        清理指定天数之前的旧备份文件
        
        Args:
            backup_dir: 备份目录
            keep_days: 保留最近多少天的备份
            
        Returns:
            int: 删除的备份文件数量
        """
        try:
            logger.info(f"开始清理 {backup_dir} 目录中 {keep_days} 天前的旧备份")
            
            import time
            cutoff_time = time.time() - (keep_days * 24 * 60 * 60)
            deleted_count = 0
            
            if os.path.exists(backup_dir):
                # 获取所有备份文件
                backups = [
                    os.path.join(backup_dir, f) 
                    for f in os.listdir(backup_dir) 
                    if f.startswith('students_backup_') and f.endswith('.json')
                ]
                
                # 删除旧备份
                for backup in backups:
                    if os.path.getmtime(backup) < cutoff_time:
                        os.remove(backup)
                        deleted_count += 1
                        logger.debug(f"删除旧备份: {backup}")
            
            logger.info(f"清理完成，删除了 {deleted_count} 个旧备份文件")
            return deleted_count
        except Exception as e:
            logger.error(f"清理旧备份失败: {str(e)}")
            return 0
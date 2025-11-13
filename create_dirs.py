import os

# 定义要创建的目录结构
dirs_to_create = [
    'src/models',
    'src/managers',
    'src/ui',
    'src/utils',
    'data'
]

# 创建目录
for dir_path in dirs_to_create:
    os.makedirs(dir_path, exist_ok=True)
    print(f'Created directory: {dir_path}')

print('All directories created successfully!')
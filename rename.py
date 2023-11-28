import os
import re

# 指定要修改的文件夹路径
folder_path = r"D:\desktop\agt_image\labels"

# 获取文件夹中所有文件的列表
file_list = os.listdir(folder_path)

# 定义一个函数，用于重命名文件
def rename_file(filename):
    if filename.endswith('.png'):
        # 使用正则表达式提取文件名中的数字部分
        match = re.search(r'(\d+)', filename)
        if match:
            # 获取匹配的数字部分
            old_number = match.group(1)
            # 将数字部分转换为整数并加上16034
            new_number = str(int(old_number) + 30159)
            # 用零补全成九位数
            new_number = new_number.zfill(9)
            # 在新的文件名中替换数字部分
            new_filename = filename.replace(old_number, new_number)
            # 构建原文件的完整路径和新文件的完整路径
            old_filepath = os.path.join(folder_path, filename)
            new_filepath = os.path.join(folder_path, new_filename)
            # 重命名文件
            os.rename(old_filepath, new_filepath)
            print(f'文件 {filename} 已重命名为 {new_filename}')
    else:
        # 如果文件不是jpg格式，删除它
        filepath = os.path.join(folder_path, filename)
        os.remove(filepath)
        print(f'文件 {filename} 已被删除')

# 遍历文件列表并调用重命名函数
for filename in file_list:
    rename_file(filename)

print("所有文件已重命名完成")



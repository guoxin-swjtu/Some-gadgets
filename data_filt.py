import os

jpg_folder = r"D:\desktop\us_ARG_data\images"
png_folder = r"D:\desktop\us_ARG_data\labels"

# 获取JPG文件夹中的所有文件名
jpg_files = set([os.path.splitext(file)[0] for file in os.listdir(jpg_folder) if file.lower().endswith('.jpg')])

# 遍历PNG文件夹中的文件
for png_file in os.listdir(png_folder):
    if png_file.lower().endswith('.png'):
        # 检查PNG文件的名称（不包含扩展名）是否不存在于JPG文件夹中
        png_name = os.path.splitext(png_file)[0]
        if png_name not in jpg_files:
            # 如果不存在，删除PNG文件
            png_file_path = os.path.join(png_folder, png_file)
            os.remove(png_file_path)
            print(f"已删除PNG文件: {png_file_path}")

print("在JPG文件夹中没有对应文件的PNG文件已被删除。")

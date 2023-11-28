import os

folder_path = r"D:\desktop\agt_image"
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension not in image_extensions:
            try:
                os.remove(file_path)
                # print(f"已删除文件: {file_path}")
            except Exception as e:
                print(f"删除文件 {file_path} 时出现错误: {str(e)}")

print("所有非图片类型文件已被删除。")

import os
from osgeo import gdal

# 输入影像文件夹路径
input_folder = r"D:\desktop\test\convert"  # 替换成包含多个四波段影像的文件夹路径
output_folder = r"D:\desktop\test\rgb"  # 替换成输出文件夹路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取文件夹中的所有TIFF文件
tiff_files = [f for f in os.listdir(input_folder) if f.endswith(".tif") or f.endswith(".tiff")]

for tiff_file in tiff_files:
    input_image_path = os.path.join(input_folder, tiff_file)
    output_image_path = os.path.join(output_folder, tiff_file)

    # 打开输入影像
    input_ds = gdal.Open(input_image_path)

    # 获取输入影像的波段数
    num_bands = input_ds.RasterCount

    # 创建输出影像
    driver = gdal.GetDriverByName("GTiff")
    output_ds = driver.Create(output_image_path, input_ds.RasterXSize, input_ds.RasterYSize, 3, gdal.GDT_Byte)

    # 复制输入影像的地理信息和投影信息到输出影像
    output_ds.SetProjection(input_ds.GetProjection())
    output_ds.SetGeoTransform(input_ds.GetGeoTransform())

    # 复制RGB波段到输出影像
    for band_num in range(1, 4):  # 复制前三个波段，即RGB
        input_band = input_ds.GetRasterBand(band_num)
        output_ds.GetRasterBand(band_num).WriteArray(input_band.ReadAsArray())

    # 保存输出影像
    output_ds.FlushCache()
    output_ds = None

    # 关闭输入影像
    input_ds = None

print("处理完成。")

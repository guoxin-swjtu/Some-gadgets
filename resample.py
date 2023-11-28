from osgeo import gdal

# 输入文件路径
input_file = "D:/desktop/dataset_utiles/geo_velocity_nearest.tif"

# 输出文件路径（不同的重采样方法将保存为不同的文件）
output_file_nearest = "D:/desktop/dataset_utiles/geo_velocity_nearest1.tif"
output_file_bilinear = "D:/desktop/dataset_utiles/geo_velocity_bilinear1.tif"
output_file_cubic = "D:/desktop/dataset_utiles/geo_velocity_cubic1.tif"
output_file_cubic_spline = "D:/desktop/dataset_utiles/geo_velocity_cubic_spline1.tif"

# 打开输入文件
ds = gdal.Open(input_file)

# 原始像素大小
original_pixel_size_x = 0.0002777777/2
original_pixel_size_y = -0.0002777777/2

# 重采样后的像素大小（原来的一半）
resampled_pixel_size_x = original_pixel_size_x / 2
resampled_pixel_size_y = original_pixel_size_y / 2

# 设置重采样选项
resample_methods = [gdal.GRA_NearestNeighbour, gdal.GRA_Bilinear, gdal.GRA_Cubic, gdal.GRA_CubicSpline]
output_files = [output_file_nearest, output_file_bilinear, output_file_cubic, output_file_cubic_spline]

for resample_method, output_file in zip(resample_methods, output_files):
    gdal.Warp(output_file, ds, format="GTiff", resampleAlg=resample_method, xRes=resampled_pixel_size_x, yRes=resampled_pixel_size_y)

# 关闭输入文件
ds = None

print("重采样完成")
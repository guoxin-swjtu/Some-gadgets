import fiona
from osgeo import gdal
from shapely.geometry import shape
from osgeo import osr

# 打开输入的 shapefile 文件
shp_path = r"D:\desktop\test\2_mountain.shp"

# 打开温度图像
temp_path = r"D:\desktop\test\temp_2.tif"
temp_ds = gdal.Open(temp_path)

# 获取温度图像的地理坐标变换信息
geo_transform = temp_ds.GetGeoTransform()

# 打开 shapefile 用于读取
with fiona.open(shp_path, 'r') as shp_src:

    # 创建一个新的 shapefile 用于写入
    schema = shp_src.schema.copy()
    schema['properties']['tmpertu'] = 'float'
    crs = shp_src.crs

    with fiona.open(r"D:\desktop\test\output_central_temperature.shp", 'w', 'ESRI Shapefile', schema, crs=crs) as shp_dst:

        for feature in shp_src:
            geom = shape(feature['geometry'])
            centroid = geom.centroid

            # 获取中心点的坐标
            x, y = centroid.xy

            # 将地理坐标转换为像素坐标
            col = int((x[0] - geo_transform[0]) / geo_transform[1])
            row = int((y[0] - geo_transform[3]) / geo_transform[5])

            # 读取温度图像的像素值
            band = temp_ds.GetRasterBand(1)
            temperature = band.ReadAsArray(col, row, 1, 1)[0][0]
            temperature=float(temperature)

            # 将温度值写入新的 shapefile
            feature['properties']['tmpertu'] = temperature
            shp_dst.write(feature)
            
print("任务完成")

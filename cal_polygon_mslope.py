from osgeo import ogr, gdal

# 设置shp文件路径和坡度图路径
shp_path = r"D:\desktop\test\1.shp"
slope_tif_path = r"D:\desktop\test\mountain_3_slope.tif"
output_shp_path = r"D:\desktop\test\output_polygon_mslope.shp"

# 打开shp文件和坡度图
shp_ds = ogr.Open(shp_path, 1)  # 1表示可写
slope_ds = gdal.Open(slope_tif_path)

if shp_ds is None:
    raise Exception(f"无法打开shp文件：{shp_path}")
if slope_ds is None:
    raise Exception(f"无法打开坡度图：{slope_tif_path}")

# 获取shp图层
shp_layer = shp_ds.GetLayer()
if shp_layer is None:
    raise Exception("找不到shp图层")

# 添加名为"slope"的字段到属性表
field_defn = ogr.FieldDefn("slope", ogr.OFTReal)
shp_layer.CreateField(field_defn)

# 逐个多边形计算坡度均值并将其添加到属性表
for feature in shp_layer:
    geom = feature.GetGeometryRef()
    envelope = geom.GetEnvelope()

    # 计算多边形所涵盖的像素坡度均值
    min_x, max_x, min_y, max_y = envelope
    col_min, row_min = slope_ds.GetGeoTransform()[1], slope_ds.GetGeoTransform()[5]
    col_offset = int((min_x - slope_ds.GetGeoTransform()[0]) / col_min)
    row_offset = int((max_y - slope_ds.GetGeoTransform()[3]) / abs(row_min))
    col_count = int((max_x - min_x) / col_min)
    row_count = int((max_y - min_y) / abs(row_min))

    slope_band = slope_ds.GetRasterBand(1)
    data = slope_band.ReadAsArray(col_offset, row_offset, col_count, row_count)
    slope_mean = data.mean()

    # 将均值添加到属性表
    feature.SetField("slope", slope_mean)
    shp_layer.SetFeature(feature)

# 保存修改后的shp文件
shp_ds.SyncToDisk()
shp_ds = None

print(f"任务完成，结果已保存到 {output_shp_path}")

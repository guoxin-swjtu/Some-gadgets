import fiona

# 打开2.shp文件用于读取
shp_path = r"D:\desktop\test\output_polygon_area.shp"
with fiona.open(shp_path, 'r') as shp_src:

    # 获取schema
    schema = shp_src.schema

    # 创建一个新的 shapefile 用于写入
    with fiona.open(r"D:\desktop\test\filtered_area_under1000.shp", 'w', 'ESRI Shapefile', schema, crs=shp_src.crs) as shp_dst:

        for feature in shp_src:
            # 读取属性表中的temperature列
            area = feature['properties']['area']

            # 只保留面积小于等于0的polygon
            if area >= 10000:
                shp_dst.write(feature)
            
print("筛选完成")

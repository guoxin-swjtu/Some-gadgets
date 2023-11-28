import fiona

# 打开2.shp文件用于读取
shp_path = "/media/xsar/F/planet_basemap_download/mountain-merge/shp/filter_all.shp"
with fiona.open(shp_path, 'r') as shp_src:

    # 获取schema
    schema = shp_src.schema

    # 创建一个新的 shapefile 用于写入
    with fiona.open("/media/xsar/F/planet_basemap_download/mountain-merge/shp/filter_all_2.shp", 'w', 'ESRI Shapefile', schema, crs=shp_src.crs) as shp_dst:

        for feature in shp_src:
            # 读取属性表中的temperature列
            temperature = feature['properties']['tempera']

            # 只保留温度小于等于0的polygon

            if temperature is None or temperature <= 10.0000:
                shp_dst.write(feature)
            
print("筛选完成")

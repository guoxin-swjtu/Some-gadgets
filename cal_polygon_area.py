import fiona
from shapely.geometry import shape
import pyproj
from shapely.ops import transform

# 打开输入的 shapefile 文件
shp_path = r"D:\desktop\test\ttt.shp"

# 选择一个适当的投影坐标系，使用 UTM 投影坐系
source_crs = pyproj.CRS("EPSG:4326")  # 输入 shapefile 的坐标系为 WGS 84

# 获取目标 UTM 投影坐标系，根据 shapefile 的中心点
with fiona.open(shp_path, 'r') as shp_src:
    minx, miny, maxx, maxy = shp_src.bounds
    
    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2
    print(minx,maxx,center_x)
    utm_zone = int((center_x + 180) / 6) + 1  # 根据中心点确定 UTM 区域

target_crs = pyproj.CRS(f"EPSG:326{utm_zone}")  # 使用计算得到的 UTM 投影坐标系

# 创建一个坐标转换器，将坐标从 WGS 84 转换为 UTM 投影坐标系
transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)

# 打开 shapefile 用于读取
with fiona.open(shp_path, 'r') as shp_src:

    # 创建一个新的 shapefile 用于写入
    schema = shp_src.schema.copy()
    schema['properties']['area'] = 'float'  # 添加一个名为 'area' 的新属性字段，并将其类型设置为浮点数

    with fiona.open(r"D:\desktop\test\output_polygon_area.shp", 'w', 'ESRI Shapefile', schema, crs=source_crs) as shp_dst:

        for feature in shp_src:
            geom = shape(feature['geometry'])

            # 使用坐标转换器将坐标从 WGS 84 转换为 UTM 投影坐标系
            projected_geom = transform(transformer.transform, geom)

            # 计算每个 polygon 的面积（平方米）
            area = projected_geom.area

            # 将面积值写入新的 shapefile
            feature['properties']['area'] = area
            shp_dst.write(feature)

print("任务完成")


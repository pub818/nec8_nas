import ezdxf

def create_full_case_dxf():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    Y_OFFSET_STEP = 300

    def add_part(points, circles=None, rect_holes=None, y_offset=0):
        shifted_points = [(p[0], p[1] + y_offset) for p in points]
        msp.add_lwpolyline(shifted_points + [shifted_points[0]])
        if circles:
            for cx, cy, r in circles:
                msp.add_circle((cx, cy + y_offset), r)
        if rect_holes:
            for x, y, w, h in rect_holes:
                p = [(x, y + y_offset), (x + w, y + y_offset), 
                     (x + w, y + h + y_offset), (x, y + h + y_offset), (x, y + y_offset)]
                msp.add_lwpolyline(p)

    # --- 1. 顶板 (Top Panel) & 2. 底板 (Bottom Panel) ---
    # 分布: 79-40(凸)-80-40(凸)-80-40(凸)-80 (总长439)
    # 侧边凹槽: 58-40(凹)-58-40(凹)-58 (总宽254, 含凸起259)
    top_outline = [
        (0, 5), (79, 5), (79, 0), (119, 0), (119, 5), (199, 5), (199, 0), (239, 0), 
        (239, 5), (319, 5), (319, 0), (359, 0), (359, 5), (439, 5), 
        (439, 259), (0, 259) 
    ]
    top_slots = [
        (0, 5+58, 5, 40), (0, 5+58+40+58, 5, 40),       # 左凹槽
        (434, 5+58, 5, 40), (434, 5+58+40+58, 5, 40),    # 右凹槽
    ]
    # 顶板 (加方孔)
    add_part(top_outline, rect_holes=top_slots + [(199.5, 49, 40, 40)], y_offset=Y_OFFSET_STEP * 3)
    # 底板
    add_part(top_outline, rect_holes=top_slots, y_offset=Y_OFFSET_STEP * 2)

    # --- 3. 背板 (Back Panel) ---
    back_outline = [(0, 0), (439, 0), (439, 94), (0, 94)]
    back_slots = [
        (79, 0, 40, 5), (199, 0, 40, 5), (319, 0, 40, 5),       # 下凹槽
        (79, 89, 40, 5), (199, 89, 40, 5), (319, 89, 40, 5),    # 上凹槽
        (0, 27, 5, 40), (434, 27, 5, 40)                        # 左右凹槽
    ]
    back_circles = []
    fan_centers = [(63.8, 47), (167.6, 47), (271.4, 47), (375.2, 47)]
    for cx, cy in fan_centers: back_circles.append((cx, cy, 38))
    screws = [(28.05, 11.25), (99.55, 11.25), (28.05, 82.75), (99.55, 82.75),
              (131.85, 11.25), (203.35, 11.25), (131.85, 82.75), (203.35, 82.75),
              (235.65, 11.25), (307.15, 11.25), (235.65, 82.75), (307.15, 82.75),
              (339.45, 11.25), (410.95, 11.25), (339.45, 82.75), (410.95, 82.75)]
    for sx, sy in screws: back_circles.append((sx, sy, 2.25))
    add_part(back_outline, circles=back_circles, rect_holes=back_slots, y_offset=Y_OFFSET_STEP)

    # --- 4. 侧板 (Side Panel) ---
    # 分布: 58-40(凸)-58-40(凸)-58 (总长254, 连凸起259)
    # 垂直分布: 22-40(凸)-22 (总宽84, 连上下凸起94)
    side_outline = [
        (0, 5), (58, 5), (58, 0), (98, 0), (98, 5), (156, 5), (156, 0), (196, 0), (196, 5), (254, 5), # 底边
        (254, 27), (259, 27), (259, 67), (254, 67), (254, 89), # 后边
        (196, 89), (196, 94), (156, 94), (156, 89), (98, 89), (98, 94), (58, 94), (58, 89), (0, 89), # 上边
        (0, 5) # 回到起点
    ]
    side_holes = [
        (33.5, 5 + 84 - 31.5, 1.5), (33.5, 5 + 84 - 31.5 - 27, 1.5), # 左侧孔
        (191, 94 - 20, 1.5), (191, 94 - 20 - 52.5, 1.5)              # 右侧孔
    ]
    # 两片侧板并排
    add_part(side_outline, circles=side_holes, y_offset=0)
    side_2_points = [(p[0] + 300, p[1]) for p in side_outline]
    side_2_holes = [(h[0] + 300, h[1], h[2]) for h in side_holes]
    add_part(side_2_points, circles=side_2_holes, y_offset=0)

    doc.saveas("Full_Case_Design_Final.dxf")
    print("全套机箱图纸已生成: Full_Case_Design_Final.dxf")

if __name__ == "__main__":
    create_full_case_dxf()

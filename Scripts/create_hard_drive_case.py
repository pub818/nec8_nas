import ezdxf

def create_hard_drive_case_v5():
    doc = ezdxf.new('R2010', setup=True)
    msp = doc.modelspace()
    
    # ==========================================
    # ### 核心参数设置 ###
    # ==========================================
    PAGE_GAP = 400.0
    # 侧板孔径改为 3.5mm (半径 1.75)，兼顾装配框量与 M3 螺丝头压持面积
    SIDE_SCREW_R = 1.75   
    FAN_SCREW_R = 2.25   # 背板风扇孔径保持 4.5mm
    # ==========================================

    def draw_part(ox, oy, name, points, circles=None, rect_holes=None):
        shifted_points = [(ox + p[0], oy + p[1]) for p in points]
        msp.add_lwpolyline(shifted_points, close=True)
        if circles:
            for cx, cy, r in circles:
                msp.add_circle((ox + cx, oy + cy), r)
        if rect_holes:
            for x, y, w, h in rect_holes:
                rect_pts = [(ox + x, oy + y), (ox + x + w, oy + y),
                            (ox + x + w, oy + y + h), (ox + x, oy + y + h)]
                msp.add_lwpolyline(rect_pts, close=True)
        if name:
            max_h = max([p[1] for p in points]) if points else 100
            msp.add_text(name, dxfattribs={'height': 12, 'insert': (ox, oy + max_h + 30)})

    # 1. 顶板/底板 (439x259)
    top_outline = [
        (0, 5), (79, 5), (79, 0), (119, 0), (119, 5), (199, 5), (199, 0), (239, 0), 
        (239, 5), (319, 5), (319, 0), (359, 0), (359, 5), (439, 5), (439, 259), (0, 259) 
    ]
    top_slots = [(0, 63, 5, 40), (0, 161, 5, 40), (434, 63, 5, 40), (434, 161, 5, 40)]

    # 2. 背板 (439x94)
    back_outline = [(0, 0), (439, 0), (439, 94), (0, 94)]
    back_slots = [(79, 0, 40, 5), (199, 0, 40, 5), (319, 0, 40, 5),
                  (79, 89, 40, 5), (199, 89, 40, 5), (319, 89, 40, 5),
                  (0, 27, 5, 40), (434, 27, 5, 40)]
    back_circles = []
    fan_centers = [(63.8, 47), (167.6, 47), (271.4, 47), (375.2, 47)]
    for cx, cy in fan_centers: back_circles.append((cx, cy, 38))
    fan_screws = [(28.05, 11.25), (99.55, 11.25), (28.05, 82.75), (99.55, 82.75),
                  (131.85, 11.25), (203.35, 11.25), (131.85, 82.75), (203.35, 82.75),
                  (235.65, 11.25), (307.15, 11.25), (235.65, 82.75), (307.15, 82.75),
                  (339.45, 11.25), (410.95, 11.25), (339.45, 82.75), (410.95, 82.75)]
    for sx, sy in fan_screws: back_circles.append((sx, sy, FAN_SCREW_R))

    # 3. 侧板 (254x84)
    side_outline = [
        (0, 5), (58, 5), (58, 0), (98, 0), (98, 5), (156, 5), (156, 0), (196, 0), (196, 5), (254, 5),
        (254, 27), (259, 27), (259, 67), (254, 67), (254, 89),
        (196, 89), (196, 94), (156, 94), (156, 89), (98, 89), (98, 94), (58, 94), (58, 89), (0, 89),
        (0, 5)
    ]
    # 应用 3.5mm 侧板孔径
    side_circles = [(33.5, 57.5, SIDE_SCREW_R), (33.5, 30.5, SIDE_SCREW_R), 
                    (191, 74, SIDE_SCREW_R), (191, 21.5, SIDE_SCREW_R)]

    # --- 垂直分布绘制 ---
    # PAGE 1: 顶板 (方孔 Y 坐标从 49 移至 29)
    draw_part(0, PAGE_GAP * 3, "PAGE 1: TOP PANEL", top_outline, rect_holes=top_slots + [(199.5, 29, 40, 40)])
    # PAGE 2: 底板
    draw_part(0, PAGE_GAP * 2, "PAGE 2: BOTTOM PANEL", top_outline, rect_holes=top_slots)
    # PAGE 3: 背板
    draw_part(0, PAGE_GAP * 1, "PAGE 3: BACK PANEL", back_outline, circles=back_circles, rect_holes=back_slots)
    # PAGE 4: 侧板
    draw_part(0, 0, "PAGE 4: SIDE PANELS", side_outline, circles=side_circles)
    draw_part(300, 0, "", side_outline, circles=side_circles)

    doc.saveas("HardDrive_Case_V5_3.5mm_Holes.dxf")
    print("生成完毕：侧板螺丝孔已优化为 3.5mm，顶板开孔已向下平移 20mm。")

if __name__ == "__main__":
    create_hard_drive_case_v5()

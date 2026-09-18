import cadquery as cq
cap_outer_diameter = 60.0
cap_height = 40.0
wall_thickness = 4.0
hole_diameter = 3.0
hole_circle_radius = 15.0
chamfer_distance = 0.5
boss_diameter = 10.0
boss_height = 8.0
tab_width = 12.0
tab_depth = 5.0
tab_height = 6.0
pocket_diameter = 20.0
pocket_depth = 5.0
pocket_margin = 5.0
base = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (cap_outer_diameter / 2, 0),
        (cap_outer_diameter / 2, cap_height - tab_height),
        (cap_outer_diameter / 2, cap_height - tab_height),
        (cap_outer_diameter / 2, cap_height),
        (0, cap_height),
    ])
    .close()
    .revolve()
)
boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    .translate((0, 0, cap_height - boss_height))
)
result = base.union(boss)
result = (
    result.faces(">Z")
    .workplane()
    .hole(hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=hole_circle_radius, count=hole_circle_radius, startAngle=0, angle=360)
    .hole(pocket_diameter, pocket_depth)
)
result = result.edges("|Z").chamfer(chamfer_distance)

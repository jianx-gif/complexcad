import cadquery as cq
total_width = 70.0
leg_height = 30.0
leg_thickness = 5.0
bar_width = total_width - 2 * bar_depth
bar_depth = 10.0
boss_radius = 12.0
boss_height = 8.0
chamfer = 0.8
hole_dia = 4.0
hole_spacing = 30.0
hole_count = 4
hole_spacing = 30.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_height, 0),
        (leg_height, leg_thickness),
        (leg_thickness, leg_thickness),
        (leg_thickness, leg_height),
        (0, leg_height),
        (0, 0)
    ])
    .close()
    .extrude(bar_depth)
)
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
)
result = base.union(boss)
result = (
    result.faces(">Z")
    .workplane()
    .center(leg_thickness/2, leg_thickness/2)
    .hole(hole_dia)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(leg_thickness/2, leg_thickness/2)
    .hole(hole_dia)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(leg_thickness/2, leg_thickness/2)
    .circle(boss_radius)
    .extrude(boss_height)
)
result = result.edges("|Z").chamfer(chamfer)

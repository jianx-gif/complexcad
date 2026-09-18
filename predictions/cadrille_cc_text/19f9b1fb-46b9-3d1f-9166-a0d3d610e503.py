import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
base_thickness = 12.0
boss_radius = 8.0
boss_height = 6.0
blind_hole_diameter = 6.0
blind_hole_depth = 8.0
rib_width = 5.0
rib_height = 8.0
rib_count = 4
chamfer_size = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter/2, 0)
    .lineTo(inner_diameter/2, base_thickness)
    .lineTo(outer_diameter/2, base_thickness)
    .lineTo(outer_diameter/2, base_thickness + boss_height)
    .lineTo(inner_diameter/2, base_thickness + boss_height)
    .lineTo(inner_diameter/2, 0)
    .close()
)
result = profile.revolve()
result = result.edges().chamfer(chamfer_size)
result = (
    result.faces(">Z")
    .workplane()
    .hole(blind_hole_diameter, blind_hole_depth)
)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=outer_diameter/2 - rib_width/2, startAngle=0, angle=360, count=6)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)

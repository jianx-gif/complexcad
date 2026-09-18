import cadquery as cq
length = 80.0
start_diameter = 15.0
wall_thickness = 2.0
vent_width = 8.0
vent_height = 3.0
chamfer_distance = 0.5
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = start_diameter / 2.0
slot_width = 1.5
slot_height = wall_thickness + 0.5
slot_depth = wall_thickness + 0.5
slot_center_x = start_diameter / 2.0 + wall_thickness / 2.0
slot_center_y = start_diameter / 2.0 + slot_depth / 2.0
result = (
    cq.Workplane("XY")
    .circle(start_diameter / 2.0)
    .extrude(length)
)
result = result.cut(slot_center_x)
result = result.edges().chamfer(chamfer_distance)
result = (
    result.faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, start_diameter/2, 0, 360)
    .hole(mount_hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, start_diameter/2, 360, 4)
    .hole(mount_hole_diameter)
)
result = result.edges().chamfer(chamfer_distance)

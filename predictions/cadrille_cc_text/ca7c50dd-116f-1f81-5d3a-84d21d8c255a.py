import cadquery as cq
base_width = 80.0
base_height = 50.0
base_thickness = 8.0
central_bore_diameter = 12.0
counterbore_diameter = 20.0
counterbore_depth = 4.0
mount_hole_diameter = 5.0
mount_hole_offset_x = 15.0
mount_hole_offset_y = 15.0
rib_thickness = 6.0
rib_height = 20.0
rib_spacing = 30.0
chamfer_size = 1.0
fillet_radius = 2.0
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_spacing)
)
base = base.union(base)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(counterbore_diameter, depth=counterbore_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_spacing)
)
result = base.union(rib)

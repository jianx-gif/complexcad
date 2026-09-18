import cadquery as cq
outer_radius = 20.0
wall_thickness = 3.0
inner_radius = outer_radius - wall_thickness
rib_width = 10.0
rib_height = 8.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(wall_thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = (
    combined.faces(">Z")
    .workplane()
    .polarArray(radius=outer_radius - wall_thickness/2, startAngle=0, count=mount_hole_spacing, angle=360)
    .hole(mount_hole_diameter)
)
combined = (
    combined.faces(">Z")
    .workplane()
    .polarArray(radius=outer_radius - wall_thickness/2, count=mount_hole_spacing, startAngle=0, angle=360)
    .hole(mount_hole_diameter)
)
result = combined

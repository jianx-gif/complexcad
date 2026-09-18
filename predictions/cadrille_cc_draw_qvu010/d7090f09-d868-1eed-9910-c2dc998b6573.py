import cadquery as cq
outer_diameter = 70.0
inner_diameter = 30.0
thickness = 15.0
wall_thickness = 2.0
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
chamfer_size = 1.0
mount_hole_dia = 4.0
mount_hole_offset = 10.0
rib_thickness = 2.0
rib_height = 5.0
rib_spacing = 12.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
inner = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(thickness)
)
base = base.cut(inner)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(mount_hole_dia)
combined = (
    combined.faces(">Z").workplane()
    .polarArray(radius=mount_hole_offset, startAngle=0, angle=360, count=rib_spacing)
    .hole(mount_hole_dia)
)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined

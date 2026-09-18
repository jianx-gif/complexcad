import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 15.0
fillet_radius = 2.0
chamfer_distance = 1.0
mount_hole_diameter = 6.0
mount_hole_offset = 10.0
rib_thickness = 4.0
rib_height = 10.0
rib_count = 6
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
base = base.edges().fillet(fillet_radius)
base = base.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rib_height)
    .translate((0, 0, thickness))
)
base = base.union(rib)
base = base.faces(">Z").workplane().hole(mount_hole_diameter)
rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_height, thickness)
    .translate((outer_radius - rib_thickness / 2.0, 0, thickness / 2.0))
)
base = base.union(rib)
base = base.edges().chamfer(chamfer_distance)
result = base

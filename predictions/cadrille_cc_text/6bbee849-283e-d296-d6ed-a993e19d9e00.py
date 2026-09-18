import cadquery as cq
outer_diameter = 80.0
block_length = 60.0
thickness = 12.0
inner_fillet = 2.0
hole_diameter = 12.0
hole_count = 8
rib_width = 10.0
rib_depth = 8.0
rib_count = 6
rib_count = 4
rib_start_z = block_length / 2.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_fillet / 2.0
inner_fillet = inner_fillet / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
base = base.edges().fillet(outer_fillet)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
rib = (
    cq.Workplane("XY")
    .center(rib_start_z, 0)
    .rect(rib_width, rib_depth)
    .extrude(rib_count)
)
base = base.union(rib)
base = base.faces(">Z").edges().fillet(inner_fillet)
base = base.faces(">Z").edges().chamfer(outer_fillet)
result = base

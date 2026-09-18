import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 2.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(outer_diameter)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(outer_diameter / 2)
    .translate((0, 0, wall_thickness))
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, wall_thickness))
)
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_distance)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2 - rib_width / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = combined

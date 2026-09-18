import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 20.0
wall_thickness = 2.0
fillet_radius = 1.0
chamfer_distance = 0.5
rib_width = 4.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 4
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius - rib_width)
    .extrude(rib_height)
    .translate((0, 0, thickness))
)
rib_pattern = rib.translate((0, 0, thickness))
rib_pattern = rib_pattern.union(rib)
rib_pattern = rib_pattern.faces(">Z").edges().chamfer(chamfer_distance)
rib_pattern = rib_pattern.faces(">Z").edges().fillet(fillet_radius)
rib_pattern = rib_pattern.faces("<Z").edges().fillet(fillet_radius)
rib_pattern = rib_pattern.faces("<Z").edges().fillet(rib_count)
result = base.union(rib_pattern)

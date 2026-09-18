import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 80.0
rib_height = 20.0
rib_width = 10.0
rib_thickness = 4.0
rib_count = 6
chamfer_size = 1.0
hole_diameter = 5.0
hole_depth = thickness / 2.0
hole_spacing = 12.0
hole_count = 4
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
rib_length = thickness / 2.0
rib_height = thickness / 2.0
rib_offset = outer_radius - rib_thickness / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness / 2.0))
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)
result = combined

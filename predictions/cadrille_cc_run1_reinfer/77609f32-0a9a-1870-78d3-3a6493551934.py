import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_width = 6.0
rib_height = 8.0
rib_thickness = 2.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_offset, hole_offset),
        (-hole_offset, hole_offset),
        (hole_offset, -hole_offset),
        (hole_offset, -hole_offset),
    ])
    .hole(hole_diameter)
)
result = combined

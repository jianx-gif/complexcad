import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 4.0
rib_width = 6.0
rib_thickness = 2.0
rib_offset = 5.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = rib.translate((rib_offset, 0, 0))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
hole_positions = [
    ( hole_offset,  hole_offset),
    (-hole_offset,  hole_offset),
    ( hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined

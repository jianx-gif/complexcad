import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 10.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(leg_length, leg_width)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = (
    rib.faces(">Z")
    .workplane()
    .center(leg_length/2 - rib_spacing/2, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
combined = base.union(rib)
hole_positions = [
    (hole_offset,  hole_offset),
    (-hole_offset,  hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

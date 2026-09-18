import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .box(leg_length, leg_width, thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
rib = (
    cq.Workplane("XY")
    .box(leg_width, leg_length, thickness)
    .translate((leg_length/2, leg_width/2, thickness/2))
)
combined = base.union(rib)
hole_positions = [
    (-hole_offset, -hole_spacing/2),
    (hole_offset, -hole_spacing/2),
    (-hole_offset, hole_spacing/2),
    (hole_offset, hole_spacing/2),
    (hole_offset, hole_spacing/2),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

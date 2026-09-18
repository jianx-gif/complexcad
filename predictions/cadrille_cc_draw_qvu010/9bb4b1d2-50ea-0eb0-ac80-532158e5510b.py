import cadquery as cq
leg_length = 70.0
leg_width = 30.0
thickness = 10.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
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
    base.faces(">Z")
    .workplane()
    .center(leg_length/2 - rib_spacing/2, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
combined = base.union(rib)
hole_positions = [
    (leg_length/2 - hole_offset, leg_width/2 - hole_offset),
    (leg_length/2 - hole_offset, leg_width/2 - hole_offset),
    (leg_length/2 - hole_offset, leg_width/2 - hole_offset),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

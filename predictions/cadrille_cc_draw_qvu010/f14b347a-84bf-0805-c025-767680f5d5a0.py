import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
rib_width = 12.0
rib_height = 6.0
rib_spacing = 15.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 0.5
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
combined = base.union(rib)
hole_positions = [
    (-leg_length/2 + hole_offset, -leg_width/2 + hole_offset),
    (leg_length/2 - hole_offset, -leg_width/2 + hole_offset),
    (leg_length/2 - hole_offset, leg_width/2 - hole_offset),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    combined
    .faces(">Z")
    .workplane()
    .center(leg_length/2 - hole_offset, 0)
    .rect(rib_width, leg_width)
    .extrude(rib_height)
)

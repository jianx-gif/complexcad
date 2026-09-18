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
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_width, 0),
        (leg_width, leg_length),
        (leg_width, leg_width),
        (0, leg_width),
        (0, 0)
    ])
    .close()
    .extrude(thickness)
)
rib = (
    base.faces(">Z").workplane()
    .center(leg_width/2, leg_length/2)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
combined = base.union(rib)
hole_positions = [
    (leg_width/2, leg_width/2),
    (leg_width/2, leg_width/2 - hole_offset),
    (leg_width/2, leg_width/2 - hole_offset),
]
result = (
    combined.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

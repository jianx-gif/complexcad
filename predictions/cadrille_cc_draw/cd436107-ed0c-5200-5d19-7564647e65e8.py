import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_edge = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_width, 0),
        (leg_width, thickness),
        (thickness, thickness),
        (thickness, leg_length),
        (0, leg_length),
        (0, 0)
    ])
    .close()
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(leg_width/2, thickness/2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = base.union(rib)
hole_positions = [
    (leg_width/2, leg_length - hole_offset_from_edge),
    (leg_width/2, leg_length - hole_offset_from_edge),
    (leg_width/2, leg_length - hole_offset_from_edge)
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

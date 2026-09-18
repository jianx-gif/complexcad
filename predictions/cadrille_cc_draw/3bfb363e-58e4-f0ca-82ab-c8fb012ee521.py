import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 15.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_width, 0),
        (leg_width, leg_length),
        (leg_width, leg_width),
        (leg_width, leg_width + leg_length),
        (0, leg_width + leg_length),
        (0, 0)
    ])
    .close()
    .extrude(thickness)
)
result = base.union(rib)
result = (
    result.faces(">Z")
    .workplane()
    .center(leg_length/2, leg_width/2)
    .rect(rib_width, rib_height)
    .cutBlind(-thickness)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(leg_width/2, leg_width/2)
    .rect(rib_width, leg_length)
    .cutBlind(-thickness)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(leg_width/2, leg_width/2)
    .rarray(hole_spacing, 0, hole_spacing, 1, center=True)
    .hole(hole_diameter)
)

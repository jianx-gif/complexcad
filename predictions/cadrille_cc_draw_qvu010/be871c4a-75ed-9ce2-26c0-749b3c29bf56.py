import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_length, 0),
        (leg_length, thickness),
        (leg_width, thickness),
        (leg_width, leg_width),
        (0, leg_width),
        (0, 0)
    ])
    .close()
    .extrude(thickness)
)
rib = (
    base.faces(">Z").workplane()
    .center(leg_length/2 - rib_spacing, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
result = base.union(rib)
result = (
    result.faces(">Z").workplane()
    .center(leg_width/2 - rib_spacing, 0)
    .rect(rib_width, rib_height)
    .cutBlind(-thickness)
)
result = (
    result.faces(">Z").workplane()
    .center(leg_width/2 - rib_spacing, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = result.edges("|Z").chamfer(chamfer_size)

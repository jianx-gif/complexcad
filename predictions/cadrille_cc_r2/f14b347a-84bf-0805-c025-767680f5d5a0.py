import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 4
result = (
    cq.Workplane("XY")
    .box(leg_length, leg_width, thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_offset, hole_offset),
        (-hole_offset, hole_offset),
        (hole_offset, hole_offset),
        (0, hole_offset),
    ])
    .hole(hole_diameter)
)

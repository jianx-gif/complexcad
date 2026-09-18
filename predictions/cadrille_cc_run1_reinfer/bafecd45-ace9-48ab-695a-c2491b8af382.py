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
    .rect(leg_length, leg_width)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(leg_width, leg_length)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(leg_width, leg_length)
    .translate((leg_length/2, leg_width/2, thickness/2))
    .extrude(thickness)
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(leg_length/2, leg_width/2)
    .rect(leg_width, leg_length)
    .cutBlind(-thickness)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(leg_length/2, leg_width/2)
    .rect(leg_width, leg_length)
    .cutBlind(-thickness)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(leg_length/2, leg_width/2)
    .rect(leg_width, leg_length)
    .cutBlind(-leg_width)
)
result = combined

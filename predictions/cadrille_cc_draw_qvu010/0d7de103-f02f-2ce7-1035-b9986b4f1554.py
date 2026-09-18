import cadquery as cq
base_length = 60.0
base_width = 30.0
base_thickness = 12.0
wall_thickness = 2.0
rib_width = 10.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_width)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, base_width)
    .cutBlind(-rib_height)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, base_width)
    .cutBlind(-rib_height)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
result = (
    combined
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

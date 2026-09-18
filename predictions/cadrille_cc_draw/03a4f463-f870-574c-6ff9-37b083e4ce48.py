import cadquery as cq
base_length = 80.0
base_width = 40.0
base_thickness = 8.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
base = (
    cq.Workplane('XY')
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
base = base.edges('|Z').fillet(base_thickness)
base = base.edges('|Z').chamfer(chamfer_size)
base = (
    base
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(hole_spacing, hole_spacing)
    .cutBlind(-hole_offset)
)
base = (
    base
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
base = (
    base
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
base = (
    base
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
result = base

import cadquery as cq
base_width = 30.0
base_thickness = 5.0
tooth_height = 10.0
tooth_pitch = 2.0
tooth_height = base_thickness + tooth_height
tooth_pitch = 2.0
chamfer = 0.3
base = (
    cq.Workplane("XY")
    .rect(base_width, base_thickness)
    .extrude(base_width)
)
base = (
    base.faces(">Z").workplane()
    .polyline([
        (-tooth_pitch/2, 0),
        (tooth_pitch/2, 0),
        (tooth_pitch/2, tooth_height),
        (tooth_pitch/2, tooth_height),
        (-tooth_pitch/2, 0),
        (-tooth_pitch/2, 0)
    ])
    .close()
    .extrude(base_width)
)
base = base.edges("|Z").chamfer(chamfer)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(tooth_pitch, tooth_height)
    .extrude(tooth_height)
)
base = base.edges("|Z").chamfer(chamfer)
result = base

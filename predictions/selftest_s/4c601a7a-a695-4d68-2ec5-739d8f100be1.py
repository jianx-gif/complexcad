import cadquery as cq

base_thickness = 5.0
base_width = 30.0
tooth_pitch = 2.0
num_teeth = 45
base_length = tooth_pitch * num_teeth
tooth_height = 10.0
chamfer = 0.3

base = cq.Workplane('XY').rect(base_length, base_width).extrude(base_thickness)

teeth = (
    base
    .faces('>Y')
    .workplane()
    .polyline([
        (-tooth_pitch/2, 0),
        (-tooth_pitch/4, tooth_height),
        (tooth_pitch/4, tooth_height),
        (tooth_pitch/2, 0),
        (-tooth_pitch/2, 0)
    ])
    .close()
    .rarray(tooth_pitch, 0, num_teeth, 1, center=True)
    .extrude(base_thickness)
)

result = base.union(teeth).edges().chamfer(chamfer)

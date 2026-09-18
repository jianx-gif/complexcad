import cadquery as cq
base_length = 80.0
base_width = 80.0
base_thickness = 5.0
base_chamfer = 0.5
frame_outer_diameter = 70.0
frame_inner_diameter = 50.0
frame_height = 10.0
frame_chamfer = 0.3
rib_thickness = 3.0
rib_height = base_thickness - frame_height
rib_length = base_length - 2 * frame_height
rib_count = 6
rib_spacing = (frame_outer_diameter - 2 * frame_height - 2 * rib_thickness) / (rib_count - 1)
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness, centered=(True, True, False))
    .edges("|Z").chamfer(base_chamfer)
)
frame = (
    base.faces(">Z").workplane()
    .circle(frame_outer_diameter / 2)
    .extrude(frame_height)
    .faces(">Z").workplane()
    .circle(frame_inner_diameter / 2)
    .extrude(frame_height)
)
frame = (
    base.faces(">Z").workplane()
    .rect(frame_height, frame_width)
    .extrude(frame_height)
)
frame = frame.edges("|Z").chamfer(base_chamfer)
frame = (
    frame.faces(">Z").workplane()
    .circle(frame_inner_diameter / 2)
    .extrude(frame_height)
)
frame = frame.edges("|Z").chamfer(frame_chamfer)
frame = (
    frame.faces(">Z").workplane()
    .polarArray(radius=frame_outer_diameter / 2 - frame_height / 2, count=rib_count, startAngle=0, angle=360)
    .rect(rib_thickness, rib_length)
    .extrude(rib_height)
)
frame = frame.edges("|Z").chamfer(base_chamfer)
result = frame

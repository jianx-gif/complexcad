import cadquery as cq
base_length = 80.0
base_width = 30.0
base_thickness = 5.0
frame_height = 10.0
frame_thickness = 5.0
frame_fillet = 0.8
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 8
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane('XY')
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
frame = (
    cq.Workplane('XY')
    .rect(frame_height, frame_thickness)
    .extrude(frame_thickness)
)
frame = (
    base
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(frame_height, frame_thickness)
    .extrude(frame_thickness)
)
frame = (
    frame
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(frame_height - 2 * frame_thickness, frame_thickness)
    .cutBlind(-frame_thickness)
)
frame = (
    frame
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(frame_height - 2 * frame_thickness, frame_thickness)
    .extrude(frame_thickness)
)
frame = (
    frame
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(frame_height - 2 * frame_thickness, frame_thickness)
    .cutBlind(-frame_thickness)
)
result = (
    frame
    .edges('|Z')
    .chamfer(chamfer_size)
)

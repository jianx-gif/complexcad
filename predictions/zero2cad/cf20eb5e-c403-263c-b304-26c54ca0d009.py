import cadquery as cq

base_length = 80.0
base_width = 60.0
base_thickness = 5.0
frame_height = 8.0
frame_thickness = 4.0
inner_length = base_length - 2 * frame_thickness
inner_width = base_width - 2 * frame_thickness

base = cq.Workplane('XY').box(base_length, base_width, base_thickness, centered=(True, True, False))
frame = (
    cq.Workplane('XY')
    .workplane(offset=base_thickness)
    .rect(base_length, base_width)
    .extrude(frame_height)
    .faces('>Z')
    .workplane()
    .rect(inner_length, inner_width)
    .cutBlind(-frame_height)
)
result = base.union(frame)

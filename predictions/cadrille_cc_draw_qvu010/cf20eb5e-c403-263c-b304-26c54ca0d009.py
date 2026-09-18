import cadquery as cq
base_length = 80.0
base_width = 60.0
base_thickness = 6.0
frame_height = 12.0
frame_thickness = 4.0
frame_fillet = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
frame = (
    cq.Workplane("XY")
    .rect(frame_length, frame_thickness)
    .extrude(frame_height)
    .translate((0, 0, base_thickness))
)
frame = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(frame_length - 2 * frame_thickness, frame_thickness)
    .cutBlind(-frame_height)
)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
frame = (
    frame
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
frame = (
    frame
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_diameter)
)
frame = (
    frame
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(frame_length - 2 * frame_thickness, frame_thickness)
    .cutBlind(-frame_height)
)
result = frame

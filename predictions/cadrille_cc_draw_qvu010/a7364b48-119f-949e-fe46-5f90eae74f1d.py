import cadquery as cq
base_length = 80.0
base_width = 50.0
base_thickness = 8.0
frame_height = 8.0
frame_thickness = 4.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_count = 6
hole_offset = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
frame = (
    cq.Workplane("XY")
    .rect(frame_height, frame_thickness)
    .extrude(frame_height)
    .translate((0, 0, base_thickness))
)
frame = frame.union(frame)
frame = frame.edges("|Z").chamfer(chamfer_size)
frame = (
    frame.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(frame_height, frame_thickness)
    .cutBlind(-frame_thickness)
)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (0, -hole_offset),
]
frame = (
    frame.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
frame = (
    frame.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(frame_height, frame_thickness)
    .cutBlind(-frame_thickness)
)
frame = (
    frame.edges("|Z")
    .chamfer(chamfer_size)
)
result = frame

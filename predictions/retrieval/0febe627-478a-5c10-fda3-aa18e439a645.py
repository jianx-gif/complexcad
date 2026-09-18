import cadquery as cq

# dimensions
base_length = 80.0
base_width = 60.0
base_thickness = 5.0
frame_outer_length = 70.0
frame_outer_width = 50.0
frame_height = 8.0
frame_wall = 4.0
rib_thickness = 2.0
rib_height = 3.0
hole_diameter = 3.0
hole_spacing = 10.0
hole_count = 5
chamfer_dist = 0.5

# derived dimensions
frame_inner_length = frame_outer_length - 2 * frame_wall
frame_inner_width = frame_outer_width - 2 * frame_wall
rib_outer_length = base_length + 2 * rib_thickness
rib_outer_width = base_width + 2 * rib_thickness
rib_cut_depth = rib_height - 0.2

# hole positions
start_x = - (frame_inner_length) / 2 + hole_spacing / 2
hole_points = [(start_x + i * hole_spacing, 0) for i in range(hole_count)]

result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness, centered=(True, True, False))
    .edges("|Z").chamfer(chamfer_dist)
    .faces(">Z")
    .workplane()
    .rect(frame_outer_length, frame_outer_width)
    .extrude(frame_height, combine=True)
    .faces(">Z")
    .workplane()
    .rect(frame_inner_length, frame_inner_width)
    .cutBlind(-frame_height)
    .faces(">Z")
    .workplane()
    .rect(rib_outer_length, rib_outer_width)
    .extrude(rib_height, combine=True)
    .faces(">Z")
    .workplane()
    .rect(base_length, base_width)
    .cutBlind(-rib_cut_depth)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)

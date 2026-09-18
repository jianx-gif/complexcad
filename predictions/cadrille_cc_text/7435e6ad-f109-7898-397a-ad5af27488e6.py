import cadquery as cq
base_radius = 30.0
base_height = 5.0
frame_thickness = 8.0
frame_length = 60.0
frame_width = 40.0
hole_diameter = 3.0
hole_offset_x = 20.0
hole_offset_y = 12.0
chamfer_base = 0.5
chamfer_frame = 0.8
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, frame_height - frame_length)
    .lineTo(frame_length, frame_height - frame_length)
    .lineTo(frame_length, frame_height)
    .lineTo(0, frame_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_base)
solid = (
    solid.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
solid = solid.edges().chamfer(chamfer_frame)
result = solid

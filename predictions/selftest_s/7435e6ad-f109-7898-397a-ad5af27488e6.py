import cadquery as cq

# Parameters
base_radius = 30.0  # radius of the revolved base (max dimension 100)
base_height = 5.0   # thickness of the base disc
frame_length = 60.0  # length of rectangular frame (X direction)
frame_width = 40.0   # width of rectangular frame (Y direction)
frame_thickness = 8.0  # height of raised frame above base
hole_diameter = 3.0  # M3 hole diameter
hole_offset_x = 20.0  # offset from frame side in X
hole_offset_y = 12.0  # offset from frame side in Y
chamfer_base = 0.5   # chamfer for base outer edge
chamfer_frame = 0.8  # chamfer for frame edges

# Revolved base profile (axisymmetric disk)
base = (
    cq.Workplane("XZ")
    .moveTo(base_radius, 0)
    .lineTo(base_radius, base_height)
    .lineTo(0, base_height)
    .close()
    .revolve()
    .edges("<Z").chamfer(chamfer_base)
)

# Add raised rectangular frame on top of the base
result = (
    base
    .faces(">Z")
    .workplane()
    .rect(frame_length, frame_width)
    .extrude(frame_thickness, combine=True)
    .edges("|Z").chamfer(chamfer_frame)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-frame_length/2 + hole_offset_x, -frame_width/2 + hole_offset_y),
        (-frame_length/2 + hole_offset_x,  frame_width/2 - hole_offset_y),
        ( frame_length/2 - hole_offset_x, -frame_width/2 + hole_offset_y),
        ( frame_length/2 - hole_offset_x,  frame_width/2 - hole_offset_y),
    ])
    .hole(hole_diameter)
)

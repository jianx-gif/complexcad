import cadquery as cq

channel_length = 80.0
channel_width = 40.0
channel_height = 30.0
wall_thickness = 3.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
countersink_diameter = 9.0
countersink_angle = 82.0
hole_spacing = 15.0
hole_rows = 2
hole_columns = 3

result = (
    cq.Workplane('XY')
    .box(channel_length, channel_width, channel_height, centered=(True, True, False))
    .shell(-wall_thickness)
    .faces('<X')
    .edges()
    .fillet(fillet_radius)
    .faces('>Y')
    .edges()
    .chamfer(chamfer_distance)
    .faces('>Z')
    .workplane()
    .rarray(hole_spacing, hole_spacing, hole_columns, hole_rows, center=True)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle)
)

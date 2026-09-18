import cadquery as cq

# Dimensions
base_length = 80.0
base_width = 60.0
base_thickness = 5.0
frame_height = 12.0
inner_length = 50.0
inner_width = 30.0
outer_top_length = 70.0
outer_top_width = 45.0
wall_thickness = 4.0
hole_diameter = 5.0
chamfer_dist = 0.5

# Base plate
result = (
    cq.Workplane('XY')
    .box(base_length, base_width, base_thickness, centered=(True, True, False))
    .edges('|Z').chamfer(chamfer_dist)
    # Move to top face to create lofted frame
    .faces('>Z')
    .workplane(offset=0)
    # Create inner rectangle profile (bottom of loft)
    .rect(inner_length, inner_width)
    .wire()
    .workplane(offset=frame_height)
    # Create outer trapezoid profile (top of loft)
    .polyline([
        (-outer_top_length/2, -outer_top_width/2),
        ( outer_top_length/2, -outer_top_width/2),
        ( outer_top_length/2,  outer_top_width/2),
        (-outer_top_length/2,  outer_top_width/2),
        (-outer_top_length/2, -outer_top_width/2)
    ])
    .close()
    .wire()
    # Loft between inner rectangle and outer trapezoid to create frame
    .loft()
    # Combine with base (the loft is already attached because workplane on base face)
    # Add four through holes at corners of inner rectangle
    .faces('>Z')
    .workplane(offset=-frame_height/2)
    .pushPoints([
        ( inner_length/2 - wall_thickness,  inner_width/2 - wall_thickness),
        (-inner_length/2 + wall_thickness,  inner_width/2 - wall_thickness),
        (-inner_length/2 + wall_thickness, -inner_width/2 + wall_thickness),
        ( inner_length/2 - wall_thickness, -inner_width/2 + wall_thickness)
    ])
    .hole(hole_diameter)
    # Add a small chamfer on upper edges of the frame for safety
    .edges('>Z and |X').chamfer(chamfer_dist)
)

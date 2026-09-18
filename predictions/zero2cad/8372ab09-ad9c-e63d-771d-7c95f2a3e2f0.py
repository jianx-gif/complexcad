import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 20.0
arm_thickness = 15.0
wall_thickness = 2.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 4
chamfer_size = 0.5

# Base cross shape (union of two perpendicular bars)
vertical_bar = cq.Workplane('XY').rect(arm_width, arm_length).extrude(arm_thickness)
horizontal_bar = cq.Workplane('XY').rect(arm_length, arm_width).extrude(arm_thickness)
base_cross = vertical_bar.union(horizontal_bar)

# Shell to create hollow interior
hollow_cross = base_cross.shell(-wall_thickness)

# Chamfer outer edges for safety
chamfered = hollow_cross.edges('>Z').chamfer(chamfer_size)

# Function to add a linear array of holes on a given face direction
def add_hole_array(part, face_selector):
    return (
        part.faces(face_selector)
        .workplane()
        .rarray(hole_spacing, 0, hole_count, 1)
        .hole(hole_diameter)
    )

# Apply hole arrays to all four side faces
with_holes = add_hole_array(chamfered, '>X')
with_holes = add_hole_array(with_holes, '<X')
with_holes = add_hole_array(with_holes, '>Y')
with_holes = add_hole_array(with_holes, '<Y')

result = with_holes
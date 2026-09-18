import cadquery as cq

# Parameter definitions
bracket_total_width = 80.0  # overall X dimension
bracket_total_height = 60.0  # overall Y dimension
bracket_thickness = 8.0  # Z thickness of material
vertical_leg_width = 12.0
vertical_leg_length = bracket_total_height
horizontal_leg_width = 12.0
horizontal_leg_length = bracket_total_width - vertical_leg_width
wall_thickness = 2.0
blind_hole_diameter = 6.0
blind_hole_depth = 5.0
blind_hole_spacing = 30.0
keyway_width = 8.0
keyway_depth = 4.0
keyway_length = 40.0
keyway_offset_from_center = 20.0
chamfer_distance = 1.0

# Build vertical leg
vertical_leg = (
    cq.Workplane("XY")
    .box(vertical_leg_width, vertical_leg_length, bracket_thickness)
)

# Build horizontal leg positioned to form L shape
horizontal_leg = (
    cq.Workplane("XY")
    .transformed(offset=(vertical_leg_width/2 + horizontal_leg_length/2, vertical_leg_length/2 - horizontal_leg_width/2, 0))
    .box(horizontal_leg_length, horizontal_leg_width, bracket_thickness)
)

# Union legs
base = vertical_leg.union(horizontal_leg)

# Shell to create hollow interior
hollow = base.shell(-wall_thickness)

# Add blind holes on vertical flange front face (+Y)
holes_face = hollow.faces(">Y")
hole_positions = [(-vertical_leg_width/4, vertical_leg_length/2 - blind_hole_spacing/2),
                (vertical_leg_width/4, vertical_leg_length/2 - blind_hole_spacing/2)]
with_holes = (
    holes_face.workplane()
    .pushPoints(hole_positions)
    .hole(blind_hole_diameter, depth=blind_hole_depth)
)

# Add keyway groove on horizontal flange bottom face (-X)
keyway_face = with_holes.faces("<X")
keyway = (
    keyway_face.workplane()
    .center(keyway_offset_from_center, 0)
    .rect(keyway_length, keyway_width)
    .cutBlind(keyway_depth)
)

# Apply chamfer to outer edges
result = (
    keyway.edges("|Z and >X or >Y")
    .chamfer(chamfer_distance)
)

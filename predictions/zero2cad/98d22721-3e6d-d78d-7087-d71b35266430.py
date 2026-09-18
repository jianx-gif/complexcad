import cadquery as cq

# Parameters
bracket_width = 60.0
bracket_height = 40.0
bracket_thickness = 8.0
corner_radius = 10.0
hole_diameter = 8.0
counterbore_diameter = 12.0
counterbore_depth = 4.0
hole_offset_x = 20.0
hole_offset_y = 15.0
chamfer_distance = 1.0
rib_width = 6.0
rib_height = 12.0
rib_spacing = 15.0
rib_depth = 2.0

# Base profile with rounded top‑right corner
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(bracket_width, 0)
    .lineTo(bracket_width, bracket_height - corner_radius)
    .threePointArc((bracket_width, bracket_height), (bracket_width - corner_radius, bracket_height))
    .lineTo(0, bracket_height)
    .close()
    .extrude(bracket_thickness)
)

# Counterbored hole on the top face
with_hole = (
    base
    .faces(">Z")
    .workplane()
    .center(hole_offset_x, hole_offset_y)
    .cboreHole(hole_diameter, counterbore_diameter, counterbore_depth)
)

# Chamfer outer vertical edges for safety
chamfered = with_hole.edges("|Z").chamfer(chamfer_distance)

# Add internal ribs on the back face for stiffness
ribbed = (
    chamfered
    .faces("<Z")
    .workplane()
    .rarray(rib_spacing, 0, int(bracket_width / rib_spacing) + 1, 1)
    .rect(rib_width, rib_height)
    .cutBlind(rib_depth)
)

result = ribbed

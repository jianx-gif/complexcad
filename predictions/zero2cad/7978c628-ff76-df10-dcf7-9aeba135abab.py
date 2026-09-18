import cadquery as cq

# Parameters
overall_width = 80.0
overall_height = 30.0
thickness = 8.0
leg_width = 12.0
leg_height = 20.0
fillet_radius = 3.0
chamfer_distance = 0.5
hole_diameter = 5.0
countersink_diameter = 9.0
countersink_angle = 82.0
hole_spacing = 20.0
rib_thickness = 2.0
rib_height = 5.0
rib_width = overall_width - 2 * leg_width - 10.0

# Base U‑shaped profile
profile = (
    cq.Workplane("XY")
    .moveTo(-overall_width / 2, 0)
    .lineTo(-overall_width / 2, leg_height)
    .lineTo(-overall_width / 2 + leg_width, leg_height)
    .lineTo(-overall_width / 2 + leg_width, overall_height)
    .lineTo(overall_width / 2 - leg_width, overall_height)
    .lineTo(overall_width / 2 - leg_width, leg_height)
    .lineTo(overall_width / 2, leg_height)
    .lineTo(overall_width / 2, 0)
    .close()
)

# Extrude to thickness
result = profile.extrude(thickness)

# Fillet inner vertical corners
result = result.edges("|Z").fillet(fillet_radius)

# Chamfer outer top edges for safety
result = result.edges(">Z").chamfer(chamfer_distance)

# Add a reinforcing rib on the back side (negative Y)
rib = (
    result.faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
result = result.union(rib)

# Countersunk holes on each leg (two per leg)
# Left leg holes
left_leg_x = -overall_width / 2 + leg_width / 2
left_leg_y_positions = [leg_height / 2 - hole_spacing / 2, leg_height / 2 + hole_spacing / 2]
for y in left_leg_y_positions:
    result = (
        result.faces(">Z")
        .workplane(centerOption="CenterOfMass")
        .center(left_leg_x, y)
        .cskHole(hole_diameter, countersink_diameter, countersink_angle, thickness)
    )
# Right leg holes
right_leg_x = overall_width / 2 - leg_width / 2
for y in left_leg_y_positions:
    result = (
        result.faces(">Z")
        .workplane(centerOption="CenterOfMass")
        .center(right_leg_x, y)
        .cskHole(hole_diameter, countersink_diameter, countersink_angle, thickness)
    )

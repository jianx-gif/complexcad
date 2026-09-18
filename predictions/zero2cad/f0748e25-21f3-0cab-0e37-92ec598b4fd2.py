import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 8.0
flange_radius = 20.0
flange_thickness = 6.0
flange_angle = 120.0
hole_diameter = 5.0
hole_clearance = 0.5
hole_spacing = 30.0
chamfer_size = 1.0
rib_height = 4.0
rib_thickness = 3.0
rib_spacing = 15.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Curved flange (revolve a rectangular profile)
flange_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(flange_radius, 0)
    .lineTo(flange_radius, flange_thickness)
    .lineTo(0, flange_thickness)
    .close()
)
flange = (
    flange_profile
    .revolve(flange_angle)
    .translate((bracket_length/2 - flange_radius, 0, 0))
)

# Combine base and flange
bracket = base.union(flange)

# Add ribs on top surface for stiffness
rib = (
    cq.Workplane("XY")
    .rect(rib_thickness, rib_height)
    .extrude(bracket_thickness)
)
num_ribs = int((bracket_length - 2 * rib_spacing) // rib_spacing) + 1
for i in range(num_ribs):
    x_pos = -bracket_length/2 + rib_spacing + i * rib_spacing
    bracket = bracket.union(rib.translate((x_pos, 0, 0)))

# Add mounting holes on the top face
hole_positions = [(-hole_spacing/2, 0), (hole_spacing/2, 0)]
for x, y in hole_positions:
    bracket = (
        bracket.faces(">Z")
        .workplane(centerOption="CenterOfMass")
        .center(x, y)
        .hole(hole_diameter + hole_clearance)
    )

# Apply chamfer to outer edges
bracket = bracket.edges("|Z").chamfer(chamfer_size)

result = bracket
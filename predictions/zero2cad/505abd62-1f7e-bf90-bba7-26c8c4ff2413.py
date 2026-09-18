import cadquery as cq

# Parameters
block_length = 80.0
block_width = 60.0
block_height = 15.0
cavity_radius = 25.0
cavity_depth = 12.0
cavity_fillet = 2.0
hole_diameter = 5.0
hole_depth = 10.0
hole_spacing_x = 30.0
hole_spacing_y = 20.0
chamfer_size = 1.0
rib_thickness = 4.0
rib_height = 5.0
rib_spacing = 20.0

# Base block with chamfered vertical edges
base = (
    cq.Workplane("XY")
    .box(block_width, block_length, block_height)
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Cavity profile (XZ plane) and revolve
cavity_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(cavity_radius, 0)
    .threePointArc((cavity_radius, cavity_depth / 2), (0, cavity_depth))
    .close()
)

cavity = cavity_profile.revolve(360)

# Subtract cavity from base
result = base.cut(cavity)

# Blind holes pattern on top face
hole_positions = [
    (-hole_spacing_x / 2, -hole_spacing_y / 2),
    (hole_spacing_x / 2, -hole_spacing_y / 2),
    (-hole_spacing_x / 2, hole_spacing_y / 2),
    (hole_spacing_x / 2, hole_spacing_y / 2),
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, depth=hole_depth)
)

# Add ribs on bottom face for stiffness
rib_count = int((block_length - rib_spacing) // rib_spacing) + 1
rib_positions = [(-block_length / 2 + rib_spacing / 2 + i * rib_spacing) for i in range(rib_count)]

for y in rib_positions:
    result = (
        result.faces("<Z")
        .workplane()
        .center(0, y)
        .rect(block_width - 2 * rib_thickness, rib_thickness)
        .extrude(-rib_height)
    )

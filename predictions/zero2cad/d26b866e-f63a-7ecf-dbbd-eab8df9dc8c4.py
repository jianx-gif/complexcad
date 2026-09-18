import cadquery as cq

# Parameters
base_width = 80.0
base_depth = 30.0
base_thickness = 8.0
flange_radius = 40.0
flange_height = 10.0
chamfer_size = 2.0
blind_hole_diameter = 6.0
blind_hole_depth = 6.0
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 20.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
)

# Flange on top of base
flange = (
    base.faces(">Z")
    .workplane()
    .circle(flange_radius)
    .extrude(flange_height)
)

# Combine base and flange
combined = base.union(flange)

# Chamfer outer vertical edges of flange
combined = combined.edges("|Z").chamfer(chamfer_size)

# Blind hole on flange (centered on one side of flange)
combined = (
    combined.faces(">Z")
    .workplane()
    .center(flange_radius - blind_hole_diameter/2, 0)
    .hole(blind_hole_diameter, blind_hole_depth)
)

# Mounting holes pattern on base plate (four holes in a square)
combined = (
    combined.faces("<Z")
    .workplane()
    .rarray(mount_hole_spacing, mount_hole_spacing, 2, 2)
    .hole(mount_hole_diameter)
)

# Ribs on underside of base for stiffness
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_depth - 2 * rib_spacing)
    .extrude(rib_height)
)

rib_positions = [
    (-base_width/2 + rib_spacing, 0),
    (base_width/2 - rib_spacing, 0)
]

for x, y in rib_positions:
    combined = combined.union(
        rib.translate((x, y, 0))
    )

result = combined
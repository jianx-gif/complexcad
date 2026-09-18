import cadquery as cq

# Parameters
base_width = 60.0
base_thickness = 8.0
arm_length = 40.0
arm_base_width = 30.0
arm_tip_width = 15.0
arm_thickness = 12.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 40.0
rib_height = 6.0
rib_thickness = 4.0
rib_offset = 10.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(base_width, base_width)
    .extrude(base_thickness)
)

# Tapered arm (loft between two rectangles)
arm = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(arm_base_width, arm_thickness)
    .workplane(offset=arm_length)
    .rect(arm_tip_width, arm_thickness)
    .loft()
)

# Combine base and arm
combined = base.union(arm)

# Fillet vertical edges of the base
combined = combined.edges("|Z").fillet(fillet_radius)

# Chamfer all edges for safety
combined = combined.edges().chamfer(chamfer_distance)

# Add mounting holes on the top face of the base
hole_positions = [(-hole_spacing/2, 0), (hole_spacing/2, 0)]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Add a reinforcing rib on the +X side of the base
rib = (
    combined.faces(">X")
    .workplane()
    .rect(rib_thickness, rib_height)
    .extrude(base_width - 2 * rib_offset)
)
combined = combined.union(rib)

result = combined
import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 6.0
leg_height = 20.0
leg_thickness = 8.0
rib_width = 6.0
rib_height = 3.0
rib_spacing = 12.0
rib_thickness = 2.0
hole_diameter = 6.0
hole_offset_x = 20.0
chamfer_size = 1.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Left leg
left_leg = (
    cq.Workplane("XY")
    .center(-bracket_length/2 + leg_thickness/2, 0)
    .rect(leg_thickness, bracket_width)
    .extrude(leg_height)
)

# Right leg
right_leg = (
    cq.Workplane("XY")
    .center(bracket_length/2 - leg_thickness/2, 0)
    .rect(leg_thickness, bracket_width)
    .extrude(leg_height)
)

# Combine base and legs
bracket = base.union(left_leg).union(right_leg)

# Chamfer outer edges before adding ribs
bracket = bracket.edges().chamfer(chamfer_size)

# Rib pattern on underside of base
rib_count = int((bracket_length - 2 * rib_spacing) // rib_spacing) + 1
rib_positions = [(-bracket_length/2 + rib_spacing + i * rib_spacing) for i in range(rib_count)]

ribs = (
    bracket.faces("<Z")
    .workplane()
    .pushPoints([(x, 0) for x in rib_positions])
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

bracket = bracket.union(ribs)

# Through hole for bolt
bracket = (
    bracket.faces(">Z")
    .workplane()
    .center(-bracket_length/2 + hole_offset_x, 0)
    .hole(hole_diameter)
)

result = bracket

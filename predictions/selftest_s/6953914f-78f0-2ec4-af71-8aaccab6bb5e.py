import cadquery as cq

# Parameters
outer_diameter = 70.0
length = 30.0
wall_thickness = 2.0
central_hole_diameter = 12.0
dimple_side = 4.0
dimple_depth = 1.5
dimple_rows = 3
dimple_cols = 5
dimple_spacing = 8.0
chamfer_distance = 0.8

# Helper to get first solid (mirroring reference technique)
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Base cylindrical shell
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(length)
    .cut(
        cq.Workplane("XY")
        .circle(inner_radius)
        .extrude(length)
    )
)

# Central clearance hole (through all length)
base = (
    base
    .faces(">Z")
    .workplane()
    .hole(central_hole_diameter)
)

# Chamfer outer edge for safety (apply to all edges of the solid)
base = (
    base
    .firstSolid()
    .edges()
    .chamfer(chamfer_distance)
)

# Tag the top workplane for later dimple pattern
base = (
    base
    .faces(">Z")
    .workplane()
    .tag("top_wp")
)

# Create hexagonal dimple pattern on top surface
points = []
start_x = -((dimple_cols - 1) * dimple_spacing) / 2.0
start_y = -((dimple_rows - 1) * dimple_spacing) / 2.0
for i in range(dimple_cols):
    for j in range(dimple_rows):
        x = start_x + i * dimple_spacing
        y = start_y + j * dimple_spacing
        points.append((x, y))

base = (
    base
    .workplaneFromTagged("top_wp")
    .pushPoints(points)
    .polygon(6, dimple_side)
    .cutBlind(dimple_depth)
)

result = base

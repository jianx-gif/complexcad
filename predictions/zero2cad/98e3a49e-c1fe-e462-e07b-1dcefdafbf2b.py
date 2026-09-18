import cadquery as cq

# Parameters
base_width = 80.0
base_depth = 50.0
base_thickness = 12.0
top_diameter = 70.0
total_height = 80.0
step_height = 10.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_spacing = 30.0
rib_thickness = 4.0
rib_height = 30.0
boss_diameter = 25.0
boss_height = 12.0

# Build lofted body
loft_builder = cq.Workplane("XY").rect(base_width, base_depth)
current_z = base_thickness
while current_z < total_height:
    t = (current_z - base_thickness) / (total_height - base_thickness)
    width = base_width * (1 - t) + top_diameter * t
    depth = base_depth * (1 - t) + top_diameter * t
    loft_builder = loft_builder.workplane(offset=step_height).rect(width, depth)
    current_z += step_height
loft_builder = loft_builder.workplane(offset=step_height).circle(top_diameter / 2)
loft_body = loft_builder.loft(combine=True)

# Base plate
base_plate = cq.Workplane("XY").rect(base_width, base_depth).extrude(base_thickness)

# Combine base and loft
result = base_plate.union(loft_body)

# Chamfer all edges
result = result.edges().chamfer(chamfer_distance)

# Mounting holes on base plate (four corners)
hole_positions = [
    (-base_width/2 + hole_spacing, -base_depth/2 + hole_spacing),
    ( base_width/2 - hole_spacing, -base_depth/2 + hole_spacing),
    (-base_width/2 + hole_spacing,  base_depth/2 - hole_spacing),
    ( base_width/2 - hole_spacing,  base_depth/2 - hole_spacing)
]
result = result.faces("<Z").workplane().pushPoints(hole_positions).hole(hole_diameter)

# Internal rib for stiffness (centered on X axis)
rib = (
    cq.Workplane("XZ")
    .rect(rib_height, rib_thickness)
    .extrude(base_depth - 2 * rib_thickness)
    .translate((0, 0, base_thickness))
)
result = result.union(rib)

# Central boss on top
boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    .translate((0, 0, total_height))
)
result = result.union(boss)

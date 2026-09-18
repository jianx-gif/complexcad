import cadquery as cq

# Parameters
hub_radius = 20.0
hub_thickness = 5.0
flange_width = 10.0
blade_root_width = 8.0
blade_root_thickness = 3.0
blade_tip_width = 20.0
blade_tip_thickness = 2.0
blade_loft_height = 40.0
blade_count = 6
fillet_radius = 0.8
chamfer_distance = 0.5

# Hub with flange
hub = (
    cq.Workplane('XY')
    .circle(hub_radius)
    .extrude(hub_thickness)
    .faces('>Z')
    .workplane()
    .circle(hub_radius + flange_width)
    .extrude(flange_width)
)

# Blade loft profile
blade = (
    cq.Workplane('XZ')
    .workplane(offset=hub_thickness + flange_width)
    .center(0, 0)
    .rect(blade_root_width, blade_root_thickness)
    .wire()
    .workplane(offset=hub_thickness + flange_width + blade_loft_height)
    .center(0, 0)
    .rect(blade_tip_width, blade_tip_thickness)
    .wire()
    .loft()
)

# Create circular array of blades manually
blade_pattern = None
for i in range(blade_count):
    angle = i * 360.0 / blade_count
    rotated = blade.rotate((0, 0, 0), (0, 0, 1), angle)
    if blade_pattern is None:
        blade_pattern = rotated
    else:
        blade_pattern = blade_pattern.union(rotated)

# Combine hub and blades
assembly = hub.union(blade_pattern)

# Apply fillet to blade outer edges and chamfer to hub flange edges
result = (
    assembly
    .edges('<Z')
    .fillet(fillet_radius)
    .edges('>Z')
    .chamfer(chamfer_distance)
)

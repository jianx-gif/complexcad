import cadquery as cq

# Parameters
outer_diameter = 80.0
inner_diameter = 60.0
rim_height = 8.0
boss_radius = 10.0
boss_height = 12.0
base_plate_radius = inner_diameter / 2 + 2.0  # 32.0
base_plate_thickness = 2.0
bridge_radius = 12.0
vent_radius = 5.0
vent_count = 8
vent_circle_radius = 30.0
rim_chamfer = 1.0
edge_chamfer = 0.5
mount_hole_diameter = 8.0
mount_hole_offset = 15.0

# Rim profile created by revolving a closed 2D sketch
rim = (
    cq.Workplane('XY')
    .moveTo(inner_diameter / 2, 0)
    .lineTo(inner_diameter / 2, rim_height)
    .lineTo(outer_diameter / 2, rim_height)
    .lineTo(outer_diameter / 2, 0)
    .close()
    .revolve()
)

# Base plate that bridges rim to central boss (starts at bottom)
base_plate = (
    cq.Workplane('XY')
    .circle(base_plate_radius)
    .extrude(base_plate_thickness)
)

# Bridge column connecting base plate to boss
bridge = (
    cq.Workplane('XY')
    .circle(bridge_radius)
    .extrude(rim_height - base_plate_thickness)
    .translate((0, 0, base_plate_thickness))
)

# Central boss extrusion placed on top of rim
boss = (
    cq.Workplane('XY')
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, rim_height))
)

# Combine all parts into a single solid
base = rim.union(base_plate).union(bridge).union(boss)

# Vent pattern: circular holes arranged on a circle around the centre
vent_pattern = (
    cq.Workplane('XY')
    .polarArray(vent_circle_radius, 0, 360, vent_count)
    .circle(vent_radius)
    .extrude(rim_height + boss_height)
)

# Subtract vents from base
with_vents = base.cut(vent_pattern)

# Mounting holes as cylinders to be cut through the part
mount_points = [(-mount_hole_offset, 0), (mount_hole_offset, 0)]
mount_holes = (
    cq.Workplane('XY')
    .pushPoints(mount_points)
    .circle(mount_hole_diameter / 2)
    .extrude(rim_height + boss_height + 2)
)

# Apply mounting holes cut
with_holes = with_vents.cut(mount_holes)

# Apply chamfers to outer rim edge and top edge of boss
result = (
    with_holes
    .edges('|Z')
    .chamfer(rim_chamfer)
    .edges('|Z')
    .chamfer(edge_chamfer)
)

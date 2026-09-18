import cadquery as cq
outer_radius = 40
inner_radius = 30
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
rib_height = 10
rib_width = 6
rib_spacing = 12
rib_count = 4
rib_count = 4
rib_count = 12
chamfer_size = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
rib_count = int(inner_radius + rib_count)
rib_count = int(inner_radius + rib_count
rib_count = rib_count * rib_spacing
rib_count = rib_count * rib_spacing
rib_positions = [rib_count + i * rib_spacing for i in range(rib_count)]
for i in range(rib_count):
    angle = i * rib_spacing
    rib_positions.append((rib_count + i * rib_spacing, rib_count))
for i in range(rib_count):
    x = rib_spacing * i
    rib_positions.append((x, rib_count))
    rib_positions.append((x, rib_count))
    rib_positions.append((x, rib_count))
rib_profile = cq.Workplane('XY').center(x, 0).rect(rib_width, rib_height).extrude(rib_height)
rib_positions = rib_positions
for i in range(rib_count):
    x = rib_spacing * math.cos(math.radians(i * 360.0 / rib_count))
    rib_positions.append((x, rib_spacing))
    rib_positions.append((x, rib_spacing))
rib_positions.append((x, rib_spacing))
result = rib_positions.union(rib_profile)

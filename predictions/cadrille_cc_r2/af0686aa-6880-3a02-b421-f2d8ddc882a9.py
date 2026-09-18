import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
base_thickness = 10.0
base_height = 8.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 30.0
hole_count = 6
hole_count = 4
hole_spacing = 12.0
hole_offset = 15.0
chamfer_distance = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(base_thickness)
inner = inner.cut(inner)
hole_positions = [hole_count - 1) * hole_spacing, 1)
hole_positions = [hole_spacing, 0, hole_count * hole_spacing]
for i in range(hole_count):
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
    hole_positions.append((hole_spacing, hole_offset))
result = hole_positions.union(hole_positions).union(1, centerOption='CenterOfBoundBox').circle(hole_diameter/2).cutBlind(-hole_depth))

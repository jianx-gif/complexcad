import cadquery as cq
outer_radius = 45.0
inner_radius = 20.0
height = 30.0
wall_thickness = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_count = 6
hole_count = 12
hole_radius = hole_diameter/2
hole_offset = 15.0
chamfer_distance = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(height)
inner = inner.cut(inner)
hole_positions = [hole_count - 1) * hole_spacing, 0, 2 * hole_count]
hole_positions = [hole_offset + i * hole_spacing, 0, hole_count]
hole_positions = [hole_offset + i * hole_spacing, hole_offset]
hole_positions = [hole_offset + i * hole_spacing, hole_offset]
hole_positions = [hole_offset + i * hole_spacing, hole_offset + i * hole_spacing]
hole_positions = [hole_offset + i * hole_spacing, hole_offset + i * hole_spacing]
hole_positions = [hole_offset + i * hole_spacing, hole_offset + i * hole_spacing]
hole_positions = [hole_offset + i * hole_spacing, hole_offset + i * hole_spacing]
hole_positions.append(hole_positions)
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset, hole_offset))
hole_positions.append((hole_offset
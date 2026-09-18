import cadquery as cq

plate_width = 80.0
plate_height = 60.0
plate_thickness = 8.0
pocket_size = 30.0
pocket_depth = 4.0
rib_width = 5.0
rib_height = 4.0
hole_diameter = 4.0
chamfer_dist = 0.8
fillet_radius = 1.0

# Base plate
base = cq.Workplane("XY").rect(plate_width, plate_height).extrude(plate_thickness)

# Central square pocket
base = base.faces('>Z').workplane().rect(pocket_size, pocket_size).cutBlind(-pocket_depth)

# Peripheral rib (raised border)
rib_outer = cq.Workplane("XY").rect(plate_width + 2 * rib_width, plate_height + 2 * rib_width).extrude(rib_height)
rib_inner = cq.Workplane("XY").rect(plate_width, plate_height).extrude(rib_height)
rib = rib_outer.cut(rib_inner)

# Combine base and rib
result = base.union(rib)

# Four holes in rib
hole_offset = (plate_width / 2) - rib_width / 2 - hole_diameter / 2
hole_positions = [
    (-hole_offset, -hole_offset),
    (hole_offset, -hole_offset),
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset)
]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)

# Chamfer outer vertical edges for safety
result = result.edges("|Z").chamfer(chamfer_dist)

# Fillet all remaining edges for stress relief
result = result.edges().fillet(fillet_radius)

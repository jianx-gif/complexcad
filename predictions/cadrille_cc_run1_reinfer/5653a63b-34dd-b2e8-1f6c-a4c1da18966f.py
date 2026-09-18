import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_width = 10.0
rib_height = 8.0
rib_thickness = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(wall_thickness)
rib = base.union(inner)
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
result = base.union(rib)
result = result.edges().chamfer(chamfer_size)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (hole_offset, -hole_spacing),
    (-hole_offset, -hole_spacing),
    (0, -hole_spacing),
]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)

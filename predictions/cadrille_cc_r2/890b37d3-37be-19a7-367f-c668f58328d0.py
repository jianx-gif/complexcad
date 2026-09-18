import cadquery as cq
outer_diameter = 80.0
inner_diameter = 60.0
thickness = 10.0
rib_height = 5.0
rib_width = 12.0
rib_thickness = 4.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_offset = 15.0
chamfer_size = 1.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = rib.translate((0, 0, thickness/2))
rib = rib.translate((0, 0, thickness/2))
combined = base.union(rib)
combined = combined.edges('|Z').chamfer(chamfer_size)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
combined = combined.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
combined = combined.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
combined = combined.faces('>Z').workplane().rect(rib_width, rib_thickness).extrude(rib_height)
combined = combined.edges('|Z').chamfer(chamfer_size)
result = combined

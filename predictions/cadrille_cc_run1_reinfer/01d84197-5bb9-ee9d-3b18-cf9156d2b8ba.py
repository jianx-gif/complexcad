import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 10.0
rib_width = 12.0
rib_height = 5.0
rib_spacing = 12.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 1.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = (cq.Workplane('XY')
       .rect(rib_width, rib_height)
       .extrude(thickness))
rib = (base.faces('>Z')
       .workplane()
       .rect(rib_width, rib_height)
       .extrude(thickness))
rib = rib.edges('|Z').chamfer(chamfer_size)
result = base.union(rib)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (0, -hole_offset),
    (-hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
    (0, -hole_offset)
]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)

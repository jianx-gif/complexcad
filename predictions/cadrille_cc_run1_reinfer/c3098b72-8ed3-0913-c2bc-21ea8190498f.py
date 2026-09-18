import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 6
hole_count = 4
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
result = result.edges('>Z').chamfer(chamfer_size)
hole_positions = [
    ( hole_spacing/2, hole_count-1),
    (-hole_spacing/2, hole_count-1),
    ( hole_spacing/2, hole_count-1),
    (-hole_spacing/2, hole_count-1),
    ( hole_spacing/2, hole_count-1),
]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)

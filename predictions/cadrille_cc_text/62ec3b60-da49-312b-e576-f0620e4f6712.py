import cadquery as cq
outer_diameter = 80.0
wall_thickness = 2.0
height = 30.0
recess_diameter = 30.0
recess_depth = 8.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
chamfer_size = 0.5
rib_thickness = 1.5
rib_height = 20.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(height)
inner_radius = outer_diameter/2 - wall_thickness
base = base.faces('>Z').workplane().circle(inner_radius).extrude(height)
base = base.faces('>Z').workplane().circle(inner_radius).extrude(height)
base = base.faces('>Z').workplane().hole(hole_diameter)
base = base.faces('>Z').edges().chamfer(chamfer_size)
rib = (cq.Workplane('XY')
       .workplane(offset=height/2)
       .rect(rib_thickness, rib_height)
       .extrude(rib_thickness))
rib = rib.translate((0, 0, wall_thickness))
base = base.union(rib)
hole_positions = [(-hole_spacing/2, hole_spacing/2), (hole_spacing/2, hole_spacing/2)]
base = base.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
base = base.faces('>Z').edges().chamfer(chamfer_size)
result = base

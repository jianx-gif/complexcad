import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 5.0
inner_radius = inner_radius - wall_thickness
rib_width = 10.0
rib_height = 8.0
rib_thickness = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 1.0
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(wall_thickness)
base = base.cut(inner)
rib = (cq.Workplane('XY')
       .rect(rib_width, rib_height)
       .extrude(wall_thickness))
rib = (base.faces('>Z')
       .workplane()
       .rect(rib_width, rib_height)
       .extrude(wall_thickness))
rib = (base.faces('>Z')
       .workplane()
       .rect(rib_width, rib_height)
       .cutBlind(-rib_thickness))
rib = (base.faces('>Z')
       .workplane()
       .rarray(hole_spacing, hole_spacing, 1, 2)
       .hole(hole_diameter)
result = rib

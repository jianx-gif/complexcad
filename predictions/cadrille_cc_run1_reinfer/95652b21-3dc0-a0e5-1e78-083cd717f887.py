import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_width = 6.0
rib_height = 8.0
rib_thickness = 2.0
rib_spacing = 12.0
hole_diameter = 5.0
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
       .extrude(rib_thickness))
rib = (base.faces('>Z')
       .workplane()
       .rect(rib_width, rib_height)
       .extrude(rib_thickness))
rib = rib.union(rib)
hole_positions = [
    ( hole_offset,  hole_offset),
    (-hole_offset,  hole_offset),
    (-hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
    ( hole_offset, -hole_offset),
    ( hole_offset, -hole_offset),
]
result = (hole_positions
          .faces('>Z')
          .workplane()
          .pushPoints(hole_positions)
          .hole(hole_diameter))

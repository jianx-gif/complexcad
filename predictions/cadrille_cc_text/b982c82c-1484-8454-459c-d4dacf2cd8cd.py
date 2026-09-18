import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_stem_width = 12.0
rib_height = 6.0
rib_top_width = 30.0
rib_top_thickness = 6.0
hole_diameter = 8.0
corner_offset = 12.0
edge_chamfer = 1.0
base = cq.Workplane('XY').box(plate_length, plate_width, plate_thickness)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_top_width, plate_length)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
base = base.union(rib)
base = base.edges('|Z').chamfer(edge_chamfer)
base = base.faces('>Z').workplane().hole(hole_diameter)
base = base.faces('>Z').workplane().hole(hole_diameter)
base = base.faces('>Z').workplane().rect(rib_top_width, plate_length).extrude(rib_height)
base = base.faces('>Z').workplane().rect(rib_top_width, plate_length).extrude(rib_height)
base = base.faces('>Z').workplane().rect(rib_top_width, plate_length).extrude(rib_height)
base = base.faces('>Z').workplane().polarArray(radius=hole_diameter/2, count=rib_top_thickness, startAngle=0, angle=360).hole(hole_diameter)
base = base.faces('>Z').workplane().pushPoints([(0, -plate_width/2 + rib_top_thickness/2), 0)]).hole(hole_diameter)
base = base.faces('>Z').workplane().pushPoints([(0, plate_width/2 - rib_top_thickness/2), 0)]).hole(rib_top_thickness)
base = base.faces('>Z').workplane().pushPoints([(0, plate_width/2 - rib_top_thickness/2), 0)]).hole(rib_stem_width)
base = base.faces('>Z').workplane().pushPoints([(0, plate_width/2), (0, -plate_width/2)])
base = base.faces('>Z').workplane().pushPoints([(0, plate_width/2), (0, plate_width/2)])
base = base.faces('>Z').workplane().pushPoints([(0, plate_width/2), (0, plate_width/2)])
base = base.faces('>Z').workplane().pushPoints([(0, plate_width/2), (0, plate_width/2)])
base = base.faces('>Z').workplane().pushPoints([(0, plate_width/2), (0, plate_width/2)])
base = base.faces('>Z').workplane().pushPoints([(0, plate_width/2), (0, plate_width/2)])
base = base.faces('<Z').workplane().pushPoints([(0, plate_width/2), (0, plate_width/2)])
base = base.faces('<Z').workplane().pushPoints([(0, plate_width/2), (0, plate_width/2)])
base = base.faces('<Z').workplane().pushPoints([(0, plate_width/2), (0, plate_width/2)])
base = base.faces('<Z').workplane().pushPoints([(0, plate_width/2), (0, plate_width/2)])
base = base.faces('<Z').workplane().pushPoints([(0, plate_width/2), (0, plate_width/2)])
result = base

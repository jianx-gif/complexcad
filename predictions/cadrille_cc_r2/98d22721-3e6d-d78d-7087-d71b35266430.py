import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
chamfer_size = 2.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_offset = 12.0
rib_width = 6.0
rib_height = 8.0
rib_thickness = 4.0
rib_spacing = 12.0
rib_count = 4
base = cq.Workplane('XY').rect(leg_length, leg_width).extrude(thickness)
base = base.edges('|Z').chamfer(chamfer_size)
hole_positions = [
    (hole_offset, leg_width/2 - hole_offset),
    (-hole_offset, leg_width/2 - hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
base = base.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, thickness/2))
)
base = base.union(rib)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (hole_offset, -hole_offset),
]
base = base.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
base = base.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
result = base

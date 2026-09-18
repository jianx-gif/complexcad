import cadquery as cq

outer_diameter = 80.0
outer_diameter = 60.0
wall_thickness = 5.0
wall_thickness = 8.0
rib_width = 4.0
rib_height = 5.0
rib_height = 2.0
rib_height = 3.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 30.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 2.0
rib_spacing = 20.0
rib_spacing = 2.0

base = (
    cq.Workplane('XY')
    .box(rib_width, rib_height, rib_height)
    .translate((0, 0, 0), (0, 0, 1), angle))
)
base = base.cut(rib_count)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_height)
rib = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_height)
rib = base.faces('>Z').workplane().hole(rib_points)
rib = rib.faces('>Z').workplane().hole(rib_points)

rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).cutBlind(-rib_thickness)
rib = rib.faces(">Z').workplane().pushPoints(hole_positions).rect(rib_width, rib_height).cutBlind(-rib_height)
result = rib.faces('>Z').workplane().pushPoints(hole_positions).rect(rib_width, rib_height).cutBlind(-rib_height)
result = result.faces(">Z').workplane().pushPoints(hole_positions).hole(hole_diameter)

result = result.faces(">Z').workplane().pushPoints(hole_offset_x, 0, 0), (0, 0, 1), angle)

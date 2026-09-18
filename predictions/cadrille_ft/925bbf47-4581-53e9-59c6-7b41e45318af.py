import cadquery as cq

outer_radius = 80.0
outer_radius = 30.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 10.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 5.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 30.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 30.0

base = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)

rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, 0))
)

rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, 0))
)

rib = rib.faces('>Z').workplane().hole(rib_points)

rib = rib.faces('>Z').workplane().hole(rib_points)

rib = rib.faces('>Z').workplane().hole(rib_points)

rib = rib.faces('>Z').workplane().pushPoints(rib_center/2, 0).rect(rib_width, rib_height).extrude(rib_height)
rib = rib.faces('>Z').workplane().hole(rib_points)

rib = rib.faces('>Z').workplane().hole(rib_points)

rib = rib.faces('>Z').workplane().pushPoints(rib_center/2, rib_count/2).rect(rib_width, rib_height).extrude(rib_height)
rib = rib.faces('>Z').workplane().hole(rib_points)
rib = rib.faces('>Z').workplane().hole(rib_points)
rib = rib.faces('>Z').workplane().hole(rib_points).translate((0, 0, rib_count))
rib = rib.faces('>Z').workplane().hole(rib_points).translate((0, 0, rib_count))
rib = rib.faces('>Z').workplane().hole(rib_points).translate((0, 0, rib_count))
rib = rib.faces('>Z').workplane().hole(rib_points).translate((0, 0, rib_count))
result = rib.faces('>Z').workplane().hole(rib_points).translate((0, 0, rib_count))
result = result.cut(rib)

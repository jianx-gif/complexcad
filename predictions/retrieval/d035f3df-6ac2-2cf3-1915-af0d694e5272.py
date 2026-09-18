import cadquery as cq

holder_length = 80.0
base_width = 30.0
mid_width = 45.0
end_width = 20.0
base_height = 20.0
mid_height = 30.0
end_height = 15.0
pocket_clearance = 2.0
hole_diameter = 10.0
fillet_radius = 1.5

outer = (
    cq.Workplane('XY')
    .rect(base_width, base_height)
    .workplane(offset=holder_length/2)
    .rect(mid_width, mid_height)
    .workplane(offset=holder_length/2)
    .rect(end_width, end_height)
    .loft(combine=True)
)

outer = outer.edges().fillet(fillet_radius)

inner = (
    cq.Workplane('XY')
    .rect(base_width - pocket_clearance, base_height - pocket_clearance)
    .workplane(offset=holder_length/2)
    .rect(mid_width - pocket_clearance, mid_height - pocket_clearance)
    .workplane(offset=holder_length/2)
    .rect(end_width - pocket_clearance, end_height - pocket_clearance)
    .loft(combine=True)
)

result = outer.cut(inner)
result = result.faces('>Z').workplane().hole(hole_diameter)

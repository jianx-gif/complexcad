import cadquery as cq

outer_diameter = 80.0
wall_thickness = 5.0
height = 40.0
lip_height = 8.0
lip_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 30.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

base = cq.Workplane('XY').circle(outer_radius).extrude(height)
hollow = base.shell(-wall_thickness)
lip = (
    cq.Workplane('XY')
    .circle(inner_radius + lip_thickness)
    .extrude(lip_height)
    .translate((0, 0, height))
)
result = hollow.union(lip)
result = result.faces('>Z').workplane().pushPoints([
    (-hole_spacing/2, -hole_spacing/2),
    (hole_spacing/2, -hole_spacing/2),
    (-hole_spacing/2, hole_spacing/2),
    (hole_spacing/2, hole_spacing/2)
]).hole(hole_diameter)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((inner_radius - rib_thickness/2, 0, height/2))
)
result = result.union(rib)
result = result.edges('|Z').chamfer(chamfer_size)

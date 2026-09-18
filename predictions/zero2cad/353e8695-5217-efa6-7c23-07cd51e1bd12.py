import cadquery as cq

outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
height = 40.0
rib_thickness = 2.0
rib_height = 30.0
rib_count = 8
chamfer_size = 1.0

outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
shell = outer_cyl.cut(inner_cyl)

rib = (
    cq.Workplane('XY')
    .box(wall_thickness, rib_thickness, rib_height)
    .translate((inner_radius + wall_thickness/2, 0, rib_height/2))
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = shell.union(ribs).faces('>Z').edges().chamfer(chamfer_size)

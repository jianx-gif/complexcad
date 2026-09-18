import cadquery as cq

outer_diameter = 60.0
wall_thickness = 3.0
length = 80.0
rib_thickness = 2.0
rib_width = 5.0
rib_count = 6
chamfer_size = 0.5

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

base = cq.Workplane('XY').circle(outer_radius).extrude(length)
shell = base.faces('>Z').shell(wall_thickness)

rib = (
    cq.Workplane('XY')
    .center(inner_radius - rib_thickness / 2.0, 0)
    .rect(rib_thickness, rib_width)
    .extrude(length)
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = shell.union(ribs).edges('|Z').chamfer(chamfer_size)

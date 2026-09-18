import cadquery as cq

outer_diameter = 80.0
length = 60.0
wall_thickness = 3.0
bore_diameter = 20.0
rib_height = 5.0
rib_width = 10.0
rib_count = 6
chamfer_size = 0.5
fillet_radius = 1.0

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

base = cq.Workplane('XY').circle(outer_radius).extrude(length)
shell = base.shell(wall_thickness)
shell = shell.faces('>Z').workplane().hole(bore_diameter)

rib = (
    cq.Workplane('XY')
    .center(inner_radius - rib_height / 2.0, 0)
    .rect(rib_height, rib_width)
    .extrude(length)
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = shell.union(ribs)
result = result.edges().chamfer(chamfer_size)
result = result.edges().fillet(fillet_radius)

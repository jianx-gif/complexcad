import cadquery as cq

outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
height = 40.0
rib_height = 5.0
rib_width = 4.0
rib_thickness = 2.0
rib_count = 3
chamfer_distance = 2.0

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height - rib_height)
    .lineTo(inner_radius + rib_width, height - rib_height)
    .lineTo(inner_radius + rib_width, height)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, 0)
    .close()
)

shell = profile.revolve()

rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_thickness)
    .translate((inner_radius + rib_width/2, 0, 0))
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = shell.union(ribs).faces(">Z").edges().chamfer(chamfer_distance)

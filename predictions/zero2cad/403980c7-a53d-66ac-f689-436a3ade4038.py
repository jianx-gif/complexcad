import cadquery as cq

outer_radius = 45.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
cap_height = 30.0
lip_height = 8.0
lip_chamfer = 2.0
rib_count = 6
rib_thickness = 2.0
rib_height = 15.0
rib_depth = wall_thickness - 1.0
rib_base_z = 5.0

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cap_height - lip_height)
    .lineTo(inner_radius, cap_height - lip_height)
    .lineTo(inner_radius, cap_height)
    .lineTo(0, cap_height)
    .close()
)

cap = profile.revolve()

cap = cap.faces(">Z").edges().chamfer(lip_chamfer)

rib = (
    cq.Workplane("XY")
    .box(rib_depth, rib_thickness, rib_height)
    .translate((inner_radius + rib_depth / 2, 0, rib_base_z + rib_height / 2))
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = cap.union(ribs)

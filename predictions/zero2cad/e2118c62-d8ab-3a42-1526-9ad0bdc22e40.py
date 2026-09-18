import cadquery as cq

outer_diameter = 80.0
wall_thickness = 5.0
length = 70.0
fillet_radius = 3.0
keyway_width = 12.0
keyway_depth = 8.0
keyway_length = 60.0
mount_hole_dia = 6.0
mount_hole_spacing = 30.0
rib_width = 10.0
rib_height = 4.0
rib_spacing = 20.0

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(length)
    .shell(-wall_thickness)
)

base = base.faces(">Z").edges().fillet(fillet_radius)

keyway = (
    cq.Workplane("XY")
    .center(outer_radius - keyway_depth / 2.0, 0)
    .box(keyway_depth, keyway_length, keyway_width)
)
base = base.cut(keyway)

hole_positions = [(-mount_hole_spacing / 2.0, 0), (mount_hole_spacing / 2.0, 0)]
for x, y in hole_positions:
    base = (
        base.faces(">Z")
        .workplane()
        .center(x, y)
        .hole(mount_hole_dia)
    )

rib_count = int((length - 2 * wall_thickness) // rib_spacing)
for i in range(rib_count):
    z_pos = wall_thickness + rib_spacing / 2.0 + i * rib_spacing
    rib = (
        cq.Workplane("XY")
        .center(inner_radius - rib_height / 2.0, 0)
        .box(rib_height, length - 2 * wall_thickness, rib_width)
        .translate((0, 0, z_pos))
    )
    base = base.cut(rib)

result = base
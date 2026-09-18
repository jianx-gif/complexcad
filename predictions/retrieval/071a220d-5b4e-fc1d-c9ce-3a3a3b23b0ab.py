import cadquery as cq

outer_radius = 40.0
inner_radius = 30.0
height = 80.0
wall_thickness = outer_radius - inner_radius
rib_width = 8.0
rib_height = 5.0
rib_thickness = 4.0
rib_spacing = 20.0
drain_hole_diameter = 6.0

main_shell = (
    cq.Workplane("XY")
    .cylinder(height, outer_radius)
    .shell(-wall_thickness)
)

num_ribs = int(height / rib_spacing)
all_ribs = None
angles = [0, 60, 120, 180, 240, 300]
for i in range(num_ribs):
    zpos = -height / 2 + rib_spacing / 2 + i * rib_spacing
    rib_base = (
        cq.Workplane("XY")
        .center(inner_radius + rib_height / 2, 0)
        .box(rib_height, rib_thickness, rib_width)
        .translate((0, 0, zpos))
    )
    rib_set = None
    for a in angles:
        rib_rot = rib_base.rotate((0, 0, 0), (0, 0, 1), a)
        rib_set = rib_rot if rib_set is None else rib_set.union(rib_rot)
    all_ribs = rib_set if all_ribs is None else all_ribs.union(rib_set)

hole = (
    cq.Workplane("YZ")
    .center(0, -height / 2 + 10)
    .cylinder(wall_thickness + 2, drain_hole_diameter / 2)
    .translate((outer_radius - wall_thickness / 2, 0, 0))
)

result = (
    main_shell
    .union(all_ribs)
    .cut(hole)
)

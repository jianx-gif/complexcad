import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
rib_width = 10.0
rib_height = 8.0
rib_thickness = 4.0
rib_spacing = 12.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
rib_count = 4
rib_count = 4
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .circle(outer_radius - rib_thickness)
        .extrude(wall_thickness)
        .translate((0, 0, wall_thickness))
    )
    base = base.union(rib)
mount_points = []
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    rib = (cq.Workplane('XY')
        .center(outer_radius - rib_thickness / 2, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness + rib_thickness)
    )
    base = base.union(rib)
mount_points = []
for i in range(1, mount_hole_spacing):
    angle = i * 360.0 / mount_hole_spacing
    rib = (cq.Workplane('XY')
        .center(outer_radius - rib_thickness / 2, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness + rib_thickness + rib_thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    mounting = rib
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    rib = (cq.Workplane('XY')
        .center(outer_radius - rib_thickness / 2, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness + rib_thickness + rib_thickness + rib_thickness + rib_height)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    mounting = rib
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    rib = (cq.Workplane('XY')
        .center(outer_radius - rib_thickness / 2, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness + rib_thickness + rib_thickness + rib_height)
        .translate((outer_radius - rib_thickness / 2, 0, wall_thickness + rib_height / 2))
    )
    rib = rib.cut(rib)
result = base.union(rib)

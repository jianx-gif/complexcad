import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_width = 10.0
rib_height = 12.0
rib_thickness = 4.0
rib_spacing = 12.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
rib_count = 4
rib_count = 2
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .circle(outer_radius - rib_thickness)
        .extrude(wall_thickness)
        .translate((0, 0, wall_thickness))
    )
    base = base.union(rib)
rib = (cq.Workplane('XY')
        .circle(inner_radius - rib_thickness)
        .extrude(wall_thickness + rib_height)
        .translate((outer_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.union(rib)
result = base.union(rib)
result = result.edges('|Z').chamfer(chamfer_size)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)

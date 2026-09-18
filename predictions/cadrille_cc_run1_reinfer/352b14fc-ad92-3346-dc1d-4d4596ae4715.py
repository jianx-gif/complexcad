import cadquery as cq
outer_radius = 45.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_width = 10.0
rib_height = 8.0
rib_thickness = 4.0
rib_spacing = 12.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_offset = 10.0
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(wall_thickness)
base = base.cut(inner)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = rib.union(rib)
rib = (base.faces('>Z')
        .workplane()
        .hole(mount_hole_diameter)
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
result = base.union(rib)
result = result.edges('|Z').chamfer(chamfer_size)

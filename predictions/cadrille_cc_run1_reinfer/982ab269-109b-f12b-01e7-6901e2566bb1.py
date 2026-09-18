import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_width = 10.0
rib_height = 8.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
rib_count = 4
rib_count = 2
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = (base.faces('>Z')
        .workplane()
        .hole(inner_radius * 2)
        .edges('|Z')
        .chamfer(chamfer_size)
    )
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = rib.union(rib)
rib = rib.edges('|Z').chamfer(chamfer_size)
result = rib

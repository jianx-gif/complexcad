import cadquery as cq
outer_diameter = 60.0
inner_diameter = 40.0
thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
rib_count = 4
rib_offset = 15.0
base = cq.Workplane('XY').circle(outer_diameter / 2).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .center(outer_diameter / 2 + rib_offset, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.edges('|Z').chamfer(chamfer_size)
rib = (
    rib.faces('>Z')
    .workplane()
    .center(outer_diameter / 2 + rib_offset, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.edges('|Z').chamfer(chamfer_size)
rib = rib.edges('|Z').chamfer(chamfer_size)
rib = (
    rib.faces('>Z')
    .workplane()
    .center(outer_diameter / 2 + rib_offset, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = rib

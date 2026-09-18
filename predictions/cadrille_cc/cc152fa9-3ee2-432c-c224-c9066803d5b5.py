import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 12.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .center(outer_diameter/2 - rib_spacing/2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((outer_diameter/2 - rib_width/2, 0, thickness/2))
rib = rib.translate((outer_diameter/2 - rib_width/2, 0, thickness/2))
result = base.union(rib)
result = result.edges('|Z').chamfer(chamfer_size)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.faces('>Z').workplane().center(0, 0).hole(mount_hole_diameter)
result = result.faces('>Z').workplane().center(0, 0).hole(mount_hole_diameter)
result = result.edges('>Z').chamfer(chamfer_size)

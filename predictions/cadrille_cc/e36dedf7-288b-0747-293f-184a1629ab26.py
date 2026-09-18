import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
wall_thickness = 5.0
rib_height = 3.0
rib_width = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(outer_diameter)
rib = (
    cq.Workplane('XY')
    .center(outer_diameter/2 - rib_thickness/2, 0)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
rib = rib.translate((0, outer_diameter/2 - rib_thickness/2, 0))
rib = rib.translate((0, outer_diameter/2 - rib_thickness/2, 0))
result = base.union(rib)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.edges('|Z').chamfer(chamfer_size)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.faces('>Z').workplane().center(0, 0).hole(mount_hole_diameter)
result = result.faces('>Z').workplane().center(0, 0).hole(mount_hole_diameter)
result = result.faces('>Z').workplane().center(0, 0).hole(mount_hole_diameter)

import cadquery as cq
outer_radius = 40.0
inner_radius = 15.0
base_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
base = cq.Workplane('XY').rect(outer_radius, outer_radius).extrude(base_thickness)
rib = (
    cq.Workplane('XY')
    .center(outer_radius - rib_width/2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, outer_radius - rib_height/2, 0))
rib = rib.translate((0, outer_radius - rib_height/2, 0))
rib = rib.translate((0, outer_radius - rib_height/2, 0))
rib = rib.translate((0, outer_radius - rib_height/2, 0))
rib = rib.translate((0, outer_radius - rib_height/2, 0))
rib = rib.translate((0, outer_radius - rib_height/2, 0))
rib = rib.translate((0, outer_radius - rib_height/2, 0))
rib = rib.translate((0, outer_radius - rib_height/2, 0))
rib = rib.translate((0, outer_radius - rib_height/2, 0))
result = rib.union(rib)
result = result.edges().chamfer(chamfer_size)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.faces('>Z').workplane().center(0, 0).hole(mount_hole_diameter)

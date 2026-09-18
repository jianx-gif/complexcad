import cadquery as cq
outer_radius = 40.0
inner_radius = 15.0
wall_thickness = 2.0
rib_height = 10.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
base = cq.Workplane('XY').rect(outer_radius, outer_radius).extrude(outer_radius)
rib = (
    cq.Workplane('XY')
    .rect(outer_radius, outer_radius)
    .extrude(rib_height)
    .translate((outer_radius - rib_width/2, 0, 0))
)
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
result = base.union(rib)
result = result.faces('>Z').edges().chamfer(chamfer_size)

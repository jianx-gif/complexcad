import cadquery as cq
outer_radius = 35
wall_thickness = 5
inner_radius = outer_radius - wall_thickness
base_thickness = 10
rib_height = 4
rib_width = 8
rib_spacing = 12
rib_count = 4
chamfer_size = 1
mount_hole_diameter = 5
mount_hole_offset = 10
base = cq.Workplane('XY').circle(outer_radius).extrude(base_thickness)
base = base.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane('XY')
    .center(outer_radius - rib_width/2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
rib = rib.translate((0, outer_radius - rib_width/2, 0))
result = rib.union(rib)

import cadquery as cq
outer_radius = 15
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
base_thickness = 10
rib_height = 6
rib_width = 4
rib_spacing = 12
rib_count = 4
chamfer_size = 0.5
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
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
result = base.union(rib)
result = result.faces('>Z').edges().chamfer(chamfer_size)
result = result.faces('>Z').edges().chamfer(chamfer_size)

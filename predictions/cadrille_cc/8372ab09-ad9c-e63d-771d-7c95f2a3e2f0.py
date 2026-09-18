import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 15.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
base = cq.Workplane('XY').rect(outer_diameter, outer_diameter).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, outer_diameter/2 + rib_height/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_height/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_height/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_height/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_height/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_height/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_height/2, 0))
result = base.union(rib)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.faces('>Z').workplane().center(0, 0).hole(mount_hole_diameter)
result = result.faces('>Z').edges().chamfer(chamfer_size)

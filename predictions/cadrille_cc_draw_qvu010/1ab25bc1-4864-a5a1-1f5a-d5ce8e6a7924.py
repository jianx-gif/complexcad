import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 20.0
rib_height = 5.0
rib_width = 10.0
rib_thickness = 2.0
rib_count = 6
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
rib_radius = outer_diameter / 2.0
rib_height = thickness - 2.0
rib_count = int(rib_height / rib_count)
base = cq.Workplane('XY').circle(outer_diameter / 2.0).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .circle(outer_diameter / 2.0)
    .extrude(thickness)
    .translate((0, 0, thickness / 2.0))
)
rib = rib.union(rib)
rib = (
    cq.Workplane('XY')
    .circle(outer_diameter / 2.0)
    .extrude(thickness)
    .translate((0, 0, thickness / 2.0))
)
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(mount_hole_diameter)
combined = combined.faces('>Z').workplane().hole(mount_hole_diameter)
combined = combined.faces('>Z').workplane().hole(mount_hole_diameter)
combined = combined.faces('>Z').workplane().polarArray(radius=mount_hole_offset, count=rib_count, startAngle=0, angle=360).hole(mount_hole_diameter)
result = combined

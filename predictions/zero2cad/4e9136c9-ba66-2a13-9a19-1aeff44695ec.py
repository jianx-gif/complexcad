import cadquery as cq

outer_diameter = 80.0
inner_diameter = 30.0
thickness = 15.0
groove_width = 5.0
groove_depth = 6.0
fillet_radius = 1.0
mount_hole_diameter = 4.0
mount_hole_count = 4
mount_hole_radius = 12.0
central_hole_diameter = 10.0
pocket_width = 10.0
pocket_height = 5.0
pocket_depth = 2.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius, groove_depth)
    .lineTo(inner_radius + groove_width, groove_depth)
    .lineTo(inner_radius + groove_width, 0)
    .close()
)

solid = profile.revolve()

solid = solid.workplane(offset=thickness).hole(central_hole_diameter)

solid = solid.workplane(offset=thickness).polarArray(radius=mount_hole_radius, startAngle=0, angle=360, count=mount_hole_count).hole(mount_hole_diameter)

solid = solid.workplane(offset=thickness).rect(pocket_width, pocket_height).cutBlind(-pocket_depth)

solid = solid.edges("|Z").fillet(fillet_radius)

result = solid
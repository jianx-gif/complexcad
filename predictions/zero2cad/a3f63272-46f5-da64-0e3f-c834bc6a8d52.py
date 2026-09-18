import cadquery as cq

outer_diameter = 90.0
inner_diameter = 70.0
cover_height = 10.0
wall_thickness = 2.0
rib_height = 2.0
rib_width = 5.0
chamfer_distance = 0.5
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

base = cq.Workplane('XY').circle(outer_radius).extrude(cover_height)
shell = base.shell(-wall_thickness)
rib = (
    cq.Workplane('XY')
    .circle(inner_radius + rib_width)
    .circle(inner_radius)
    .extrude(rib_height)
    .translate((0, 0, cover_height - rib_height))
)
combined = shell.union(rib)
combined = combined.faces('>Z').edges().chamfer(chamfer_distance)
result = (
    combined
    .faces('>Z')
    .workplane()
    .rarray(mount_hole_spacing, mount_hole_spacing, 2, 2)
    .hole(mount_hole_diameter)
)

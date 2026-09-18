import cadquery as cq

overall_length = 80
overall_width = 30
overall_height = 20
wall_thickness = 3
fillet_radius = 2
chamfer_depth = 1
circle_diameter = 15
mount_hole_diameter = 5
mount_hole_spacing = 30
mount_hole_count = 3

inner_width = overall_width - 2 * wall_thickness
inner_height = overall_height - 2 * wall_thickness
rib_width = inner_width * 0.6
rib_height = inner_height * 0.6
rib_length = overall_length - 2 * wall_thickness

base = (
    cq.Workplane("XY")
    .sketch()
    .rect(overall_width, overall_height, mode="a")
    .circle(circle_diameter, mode="a")
    .finalize()
    .extrude(overall_length)
)

base_fillet = base.edges("|Z").fillet(fillet_radius)

shelled = base_fillet.shell(-wall_thickness)

rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_length)
    .translate((0, 0, wall_thickness))
)

combined = shelled.union(rib)

combined = (
    combined.faces("<X")
    .workplane()
    .rarray(mount_hole_spacing, 0, mount_hole_count, 1)
    .hole(mount_hole_diameter)
    .faces(">X")
    .workplane()
    .rarray(mount_hole_spacing, 0, mount_hole_count, 1)
    .hole(mount_hole_diameter)
)

combined = combined.faces(">Z").edges().chamfer(chamfer_depth)
combined = combined.faces("<Z").edges().chamfer(chamfer_depth)

result = combined
import cadquery as cq
overall_length = 80.0
overall_width = 30.0
overall_height = 20.0
wall_thickness = 3.0
fillet_radius = 2.0
chamfer_depth = 1.0
mount_hole_diameter = 15.0
mount_hole_spacing = 30.0
mount_hole_count = 4
mount_hole_radius = wall_thickness + 2.0
mount_hole_count = 4
mount_hole_radius = mount_hole_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(overall_length)
    .extrude(overall_height)
    .shell(-wall_thickness)
)
base = base.edges("|Z").fillet(fillet_radius)
base = base.edges().chamfer(chamfer_depth)
mount_points = [
    (mount_hole_radius * math.cos(math.radians(a)), mount_hole_radius * math.sin(math.radians(a))) for a in mount_hole_count)]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(mount_hole_radius * math.cos(math.radians(a))) for a in mount_hole_count)
    .hole(mount_hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(mount_hole_radius * math.cos(math.radians(a))) for a in mount_hole_count)
    .hole(mount_hole_diameter)
)
base = base.edges("|Z").chamfer(chamfer_depth)
result = base

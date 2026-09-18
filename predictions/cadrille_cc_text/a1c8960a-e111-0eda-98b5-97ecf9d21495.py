import cadquery as cq
overall_diameter = 80.0
overall_thickness = 10.0
central_hole_diameter = 20.0
recess_diameter = 30.0
recess_depth = 4.0
outer_fillet_radius = 1.0
mount_hole_diameter = 5.0
mount_hole_offset_radius = 30.0
rib_width = 6.0
rib_length = 40.0
rib_height = 4.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .circle(overall_diameter / 2)
    .extrude(overall_thickness)
)
base = base.edges("|Z").fillet(outer_fillet_radius)
base = base.edges(">Z").chamfer(chamfer_distance)
base = (
    base.faces(">Z").workplane()
    .circle(central_hole_diameter / 2)
    .cutBlind(-recess_depth)
)
base = (
    base.faces(">Z").workplane()
    .circle(central_hole_diameter / 2)
    .cutBlind(-recess_depth)
)
base = (
    base.faces(">Z").workplane()
    .polarArray(radius=mount_hole_offset_radius, startAngle=0, angle=360, count=mount_hole_offset)
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
base = base.union(base)
base = (
    base.faces(">Z").workplane()
    .polarArray(radius=mount_hole_offset_radius, count=mount_hole_offset, angle=360, startAngle=0, angle=360)
    .hole(mount_hole_diameter)
)
result = base

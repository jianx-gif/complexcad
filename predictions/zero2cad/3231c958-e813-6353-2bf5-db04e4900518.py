import cadquery as cq

outer_diameter = 80.0
inner_diameter = 40.0
thickness = 10.0
chamfer_size = 2.0
blind_hole_diameter = 12.0
blind_hole_depth = 6.0
groove_width = 4.0
groove_depth = 2.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = outer_diameter/2 - 5.0
rib_width = 6.0
rib_height = 2.0
rib_count = 6
rib_radius = inner_diameter/2 + 5.0
outer_chamfer = 1.0

base = (
    cq.Workplane("XY")
    .circle(outer_diameter/2)
    .circle(inner_diameter/2)
    .extrude(thickness)
)

base = base.faces("<Z").edges().chamfer(chamfer_size)

base = base.faces(">Z").edges().chamfer(outer_chamfer)

base = base.faces(">Z").workplane().hole(blind_hole_diameter, blind_hole_depth)

base = (
    base.faces(">Z")
    .workplane()
    .circle(outer_diameter/2 - groove_width/2)
    .circle(outer_diameter/2 - groove_width/2 - groove_width)
    .cutBlind(groove_depth)
)

base = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, startAngle=0, angle=360, count=mount_hole_count)
    .hole(mount_hole_diameter)
)

base = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=rib_radius, startAngle=0, angle=360, count=rib_count)
    .rect(rib_width, rib_height)
    .cutBlind(rib_height)
)

result = base
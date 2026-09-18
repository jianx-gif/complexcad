import cadquery as cq
rail_length = 80
rail_height = 20
outer_width = 30
corner_radius = 4
guide_width = 6
guide_depth = 8
central_hole_dia = 10
mount_hole_dia = 4
mount_hole_offset = 10
rib_width = 8
rib_height = 3
rib_length_factor = 0.8
chamfer_dist = 0.8
base = (
    cq.Workplane("YZ")
    .rect(outer_width, rail_height)
    .extrude(rail_length)
)
base = base.edges("|Z").fillet(corner_radius)
base = (
    base.faces(">Z").workplane()
    .rect(guide_width, guide_depth)
    .cutBlind(-guide_depth)
)
base = base.cut(
    cq.Workplane("XZ")
    .center(0, 0)
    .circle(central_hole_dia/2)
    .extrude(rail_length)
)
base = (
    base.faces(">Z").workplane()
    .pushPoints([(-rail_length/2 + mount_hole_offset, 0), (rail_length/2 - mount_hole_offset, 0)])
    .hole(mount_hole_dia)
)
rib_length = rail_length * rib_length_factor
rib = (
    cq.Workplane("XY", origin=(0, 0, -rail_height/2))
    .center(-rail_length/2 + rib_length/2, 0)
    .rect(rib_length, rib_width)
    .extrude(rib_height)
)
base = base.union(rib)
base = base.edges("|X").chamfer(chamfer_dist)
result = base
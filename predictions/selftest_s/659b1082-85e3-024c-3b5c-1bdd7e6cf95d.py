import cadquery as cq

outer_dia = 80.0
inner_dia = 40.0
wall_thk = 5.0
seat_depth = 10.0
block_len = 60.0
pin_hole_dia = 12.0
pin_hole_offset = inner_dia/2 + wall_thk/2
arc_offset = 5.0
boss_dia_factor = 0.6
mount_hole_dia = 6.0
mount_spacing = 30.0
keyway_width = 5.0
keyway_depth = 8.0
flange_thk = 4.0
flange_dia = 70.0

outer_rad = outer_dia/2
inner_rad = inner_dia/2

result = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(outer_rad, 0)
    .lineTo(outer_rad, block_len)
    .lineTo(inner_rad + wall_thk, block_len)
    .threePointArc(
        (inner_rad + wall_thk - seat_depth/2, block_len - seat_depth/2 + arc_offset),
        (inner_rad + wall_thk - seat_depth, block_len - seat_depth)
    )
    .lineTo(0, block_len - seat_depth)
    .close()
    .revolve()
)

flange = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(flange_dia/2)
    .circle((flange_dia - 2*flange_thk)/2)
    .extrude(flange_thk)
)

result = result.union(flange)

boss = (
    cq.Workplane("XZ")
    .center(pin_hole_offset, block_len/2)
    .circle(pin_hole_dia * boss_dia_factor / 2)
    .extrude(wall_thk)
)

result = result.union(boss)

hole_cyl = (
    cq.Workplane("XZ")
    .center(pin_hole_offset, block_len/2)
    .circle(pin_hole_dia/2)
    .extrude(outer_rad*2)
)

result = result.cut(hole_cyl)

counterbore_cut = (
    cq.Workplane("XZ")
    .center(pin_hole_offset, block_len/2)
    .circle(pin_hole_dia*0.75/2)
    .extrude(-wall_thk)
)

result = result.cut(counterbore_cut)

keyway = (
    cq.Workplane("YZ")
    .center(outer_rad - keyway_depth/2, block_len/2)
    .rect(keyway_depth, keyway_width)
    .extrude(keyway_width)
)

result = result.cut(keyway)

mount_holes = (
    result.faces(">Y").workplane()
    .pushPoints([
        (-mount_spacing/2, block_len/4),
        (mount_spacing/2, block_len/4),
        (-mount_spacing/2, -block_len/4),
        (mount_spacing/2, -block_len/4)
    ])
    .hole(mount_hole_dia)
)

result = mount_holes

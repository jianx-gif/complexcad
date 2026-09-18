import cadquery as cq

# Parameters
outer_radius = 45.0
inner_radius = 30.0
pulley_width = 20.0
groove_depth = 2.0
groove_width = 4.0
keyway_width = 5.0
keyway_depth = 6.0
keyway_length = 12.0
chamfer_size = 0.5
mount_hole_dia = 5.0
mount_hole_spacing = 30.0
flange_extra = 4.0
flange_thickness = 2.0

# Base pulley body (cylindrical shell)
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(pulley_width)
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(pulley_width)
)

# Chamfer outer rim edges (top and bottom)
base = base.edges("<<Z").chamfer(chamfer_size)

# Groove cut (circumferential groove on outer surface)
groove = (
    cq.Workplane("XY")
    .circle(outer_radius - groove_depth)
    .extrude(groove_width)
    .translate((0, 0, (pulley_width - groove_width) / 2))
)
base = base.cut(groove)

# Keyway cut (rectangular slot on inner surface)
keyway = (
    cq.Workplane("XY")
    .box(keyway_depth, keyway_width, keyway_length)
    .translate((inner_radius - keyway_depth / 2, 0, (pulley_width - keyway_length) / 2))
)
base = base.cut(keyway)

# Mounting holes on outer face (two opposite holes)
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing / 2, 0), (mount_hole_spacing / 2, 0)])
    .hole(mount_hole_dia)
)

# Flange on outer face for added rigidity
flange = (
    cq.Workplane("XY")
    .circle(outer_radius + flange_extra)
    .extrude(flange_thickness)
    .translate((0, 0, pulley_width))
)
base = base.union(flange)

result = base
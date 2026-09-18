import cadquery as cq

# Dimensions (units up to 100)
housing_base_width = 80.0
housing_base_length = 60.0
housing_base_height = 40.0
step_height = 8.0
num_loft_steps = 4
scale_factor = 0.85
rib_thickness = 3.0
rib_width_ratio = 0.25
mount_rib_height = 12.0
mount_rib_thickness = 4.0
mount_rib_width = 5.0
mount_rib_fillet = 1.0
cutout_width = 14.0
cutout_height = 20.0
cutout_depth = housing_base_width / 2.0
fillet_radius = 1.5

# Build lofted housing body
body = cq.Workplane('XY').rect(housing_base_width, housing_base_length)
for i in range(1, num_loft_steps):
    width_i = housing_base_width * (scale_factor ** i)
    length_i = housing_base_length * (scale_factor ** i)
    body = body.workplane(offset=i * step_height).rect(width_i, length_i)
body = body.loft(combine=True)

# Add internal rib (union)
rib_width = housing_base_width * rib_width_ratio
rib = (
    cq.Workplane('XY')
    .rect(rib_width, housing_base_length * 0.9)
    .extrude(rib_thickness)
    .translate((0, 0, housing_base_height * 0.05))
)
body = body.union(rib)

# Create mounting rib pockets on +X side (cut) and fillet their edges
for z in [housing_base_height * 0.3, housing_base_height * 0.6, housing_base_height * 0.9]:
    rib_pocket = cq.Workplane('YZ')\
        .rect(mount_rib_height, mount_rib_thickness)\
        .extrude(mount_rib_width)\
        .translate((housing_base_width / 2.0 - mount_rib_width, 0, z - housing_base_height * 0.05))
    body = body.cut(rib_pocket)
# Fillet edges of rib pockets
body = body.edges(">X").fillet(mount_rib_fillet)

# Cutouts on -Y face (arrayed vertically)
cutout = (
    cq.Workplane('XY')
    .rect(cutout_width, cutout_height)
    .extrude(cutout_depth)
    .translate((0, -housing_base_length / 2.0 - cutout_depth / 2.0, 0))
)
cutouts = cq.Workplane('XY')
for z in [housing_base_height * 0.25, housing_base_height * 0.55, housing_base_height * 0.85]:
    cutouts = cutouts.union(cutout.translate((0, 0, z)))
body = body.cut(cutouts)

# Small fillet on top edges for safety
body = body.edges(">Z").fillet(fillet_radius)

result = body
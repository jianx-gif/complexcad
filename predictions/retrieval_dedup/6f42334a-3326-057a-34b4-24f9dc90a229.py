import cadquery as cq

# Parameters
arm_length = 80.0
arm_radius = 10.0
wall_thickness = 2.0
inner_radius = arm_radius
outer_radius = arm_radius + wall_thickness
protrusion_width = 6.0
protrusion_height = 6.0
protrusion_position = 40.0
hole_diameter = 4.0
hole_depth = wall_thickness - 0.5
bevel_depth = 1.0
rib_thickness = 1.5
rib_width = 4.0
rib_height = 8.0
mount_hole_diameter = 3.0
mount_hole_spacing = 20.0

# Base profile for revolve (XY plane, revolve around Z)
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, protrusion_position)
    .lineTo(inner_radius + protrusion_width, protrusion_position)
    .lineTo(inner_radius + protrusion_width, protrusion_position + protrusion_height)
    .lineTo(inner_radius, protrusion_position + protrusion_height)
    .lineTo(inner_radius, arm_length)
    .lineTo(outer_radius, arm_length)
    .lineTo(outer_radius, 0)
    .lineTo(inner_radius, 0)
    .close()
)

result = profile.revolve(360)

blind_hole = (
    cq.Workplane("XY")
    .center(inner_radius + wall_thickness/2, arm_length/2)
    .circle(hole_diameter/2)
    .extrude(-hole_depth)
)
result = result.cut(blind_hole)

rib = (
    cq.Workplane("XY")
    .center(outer_radius, rib_height/2)
    .rect(rib_thickness, rib_height)
    .extrude(rib_width)
)
result = result.union(rib)

mount_holes = None
for offset in [-mount_hole_spacing/2, 0, mount_hole_spacing/2]:
    cyl = (
        cq.Workplane("XY")
        .center(inner_radius + wall_thickness/2, offset)
        .circle(mount_hole_diameter/2)
        .extrude(wall_thickness + 0.2)
        .rotate((0, 0, 0), (0, 0, 1), 90)
    )
    mount_holes = cyl if mount_holes is None else mount_holes.union(cyl)
result = result.cut(mount_holes)

bevel_cut = (
    cq.Workplane("XY")
    .center(0, arm_length - bevel_depth/2)
    .rect(outer_radius*2, bevel_depth)
    .extrude(bevel_depth)
)
result = result.cut(bevel_cut)

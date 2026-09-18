import cadquery as cq

# Parameters
outer_diameter = 30.0
cap_thickness = 8.0
central_aperture_dia = 6.0
inner_fillet_radius = 2.0
outer_chamfer = 0.8
mount_hole_dia = 4.0
mount_hole_count = 6
mount_hole_radius = 10.0
boss_diameter = 10.0
boss_height = 4.0
rib_width = 2.0
rib_height = 3.0
rib_depth = 2.0
rib_count = 8
vent_slot_width = 1.5
vent_slot_length = 12.0
vent_slot_count = 4
vent_radius = 12.0

# Base disc
result = (
    cq.Workplane('XY')
    .circle(outer_diameter / 2)
    .extrude(cap_thickness)
)

# Central aperture with inner fillet via cut cylinder with fillet
cylinder_cut = (
    cq.Workplane('XY')
    .circle(central_aperture_dia / 2)
    .extrude(cap_thickness)
    .edges()
    .fillet(inner_fillet_radius)
)
result = result.cut(cylinder_cut)

# Mounting holes around a circle
result = (
    result
    .faces('>Z')
    .workplane()
    .polarArray(mount_hole_radius, 0, 360 / mount_hole_count, mount_hole_count)
    .hole(mount_hole_dia)
)

# Central boss without fillet
result = (
    result
    .faces('>Z')
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Ventilation slots cut into top surface before adding ribs
for i in range(vent_slot_count):
    angle = 360.0 / vent_slot_count * i
    result = (
        result
        .faces('>Z')
        .workplane()
        .center(vent_radius, 0)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .rect(vent_slot_width, vent_slot_length)
        .cutBlind(-cap_thickness + 0.5)
    )

# Define rib profile
rib_profile = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
)

# Add radial ribs around outer periphery
for i in range(rib_count):
    angle = 360.0 / rib_count * i
    rib = (
        rib_profile
        .translate((outer_diameter / 2 - rib_depth / 2, 0, 0))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(rib)

# Outer rim chamfer applied after all features
result = result.edges('>Z').chamfer(outer_chamfer)

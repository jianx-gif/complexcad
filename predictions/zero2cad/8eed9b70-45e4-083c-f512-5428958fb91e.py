import cadquery as cq

# Parameters
outer_radius = 45.0
wall_thickness = 2.0
cover_height = 30.0
lip_height = 5.0
lip_thickness = 3.0
chamfer_size = 1.0
mount_hole_dia = 5.0
mount_hole_count = 4
mount_hole_radius = outer_radius - wall_thickness/2
vent_slot_width = 5.0
vent_slot_length = 20.0
vent_slot_depth = 2.0
boss_radius = 4.0
boss_height = 6.0
rib_thickness = 1.5
rib_height = 10.0
rib_count = 6

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cover_height)
    .threePointArc((outer_radius + lip_thickness, cover_height + lip_height/2), (outer_radius + lip_thickness, cover_height + lip_height))
    .lineTo(0, cover_height + lip_height)
    .close()
)

# Revolve to create solid
solid = profile.revolve()

# Shell to create thin wall
hollow = solid.shell(-wall_thickness)

# Chamfer outer lip edge
hollow = hollow.faces(">Z").edges().chamfer(chamfer_size)

# Add mounting holes on top face
hollow = (
    hollow.faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, startAngle=0, angle=360, count=mount_hole_count)
    .hole(mount_hole_dia)
)

# Add vent slot on top face
hollow = (
    hollow.faces(">Z")
    .workplane()
    .center(0, -cover_height/4)
    .rect(vent_slot_width, vent_slot_length)
    .cutBlind(-vent_slot_depth)
)

# Add internal boss for reinforcement
hollow = (
    hollow.faces("<Z")
    .workplane()
    .center(outer_radius - wall_thickness/2, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)

# Add internal ribs (radial) evenly spaced
angle_step = 360 / rib_count
for i in range(rib_count):
    rib = (
        cq.Workplane("XY")
        .center(outer_radius - wall_thickness/2, 0)
        .rect(rib_thickness, rib_height)
        .extrude(wall_thickness)
        .rotate((0, 0, 0), (0, 0, 1), i * angle_step)
    )
    hollow = hollow.union(rib)

result = hollow
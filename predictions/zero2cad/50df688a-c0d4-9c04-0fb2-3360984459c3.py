import cadquery as cq

outer_diameter = 80.0
inner_diameter = 20.0
hub_diameter = 30.0
hub_height = 15.0
pulley_width = 20.0
fillet_radius = 2.5
mount_hole_diameter = 5.0
mount_hole_count = 6
mount_hole_radius = 35.0
keyway_width = 6.0
keyway_depth = 4.0
keyway_length = 20.0
rib_width = 8.0
rib_height = 5.0
rib_count = 4

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
hub_radius = hub_diameter / 2.0

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, hub_height)
    .lineTo(hub_radius, hub_height)
    .lineTo(hub_radius, hub_height + 5)
    .lineTo(outer_radius, hub_height + 5)
    .lineTo(outer_radius, hub_height + 5 + pulley_width)
    .lineTo(inner_radius, hub_height + 5 + pulley_width)
    .close()
)

result = profile.revolve()

result = result.edges().fillet(fillet_radius)

result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360)
    .hole(mount_hole_diameter)
)

result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360)
    .rect(keyway_width, keyway_length)
    .cutBlind(-keyway_depth)
)

result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=outer_radius - rib_width/2, count=rib_count, startAngle=0, angle=360)
    .rect(rib_width, pulley_width)
    .cutBlind(-rib_height)
)

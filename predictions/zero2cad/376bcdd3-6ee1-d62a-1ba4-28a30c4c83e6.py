import cadquery as cq
import math

outer_radius = 45.0
inner_radius = 35.0
cover_height = 20.0
lip_height = 5.0
fillet_radius = 2.0
vent_slot_width = 4.0
vent_slot_height = 10.0
vent_slot_depth = 2.0
vent_slot_count = 12
mount_hole_diameter = 5.0
mount_hole_offset = 10.0

profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, cover_height - lip_height)
    .lineTo(outer_radius, cover_height - lip_height)
    .lineTo(outer_radius, cover_height)
    .lineTo(inner_radius, cover_height)
    .close()
)

solid = profile.revolve()

solid = solid.edges().fillet(fillet_radius)

slot_radius = outer_radius - vent_slot_depth / 2.0
points = [
    (
        slot_radius * math.cos(math.radians(i * 360.0 / vent_slot_count)),
        slot_radius * math.sin(math.radians(i * 360.0 / vent_slot_count))
    )
    for i in range(vent_slot_count)
]

solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(points)
    .rect(vent_slot_width, vent_slot_height)
    .cutBlind(-vent_slot_depth)
)

hole_radius = mount_hole_diameter / 2.0
hole_distance = outer_radius - mount_hole_offset
hole_points = [
    (
        hole_distance * math.cos(math.radians(i * 360.0 / 4)),
        hole_distance * math.sin(math.radians(i * 360.0 / 4))
    )
    for i in range(4)
]

solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(mount_hole_diameter)
)

result = solid
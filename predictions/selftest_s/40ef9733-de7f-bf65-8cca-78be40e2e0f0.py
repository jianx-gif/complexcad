import cadquery as cq

cone_height = 80
base_radius = 40
wall_thickness = 2
tip_radius = 1
vent_slot_width = 4
vent_slot_height = 12
vent_slot_offset = 15
mount_hole_diameter = 5

solid_cone = (
    cq.Workplane("XY")
    .moveTo(tip_radius, tip_radius)
    .lineTo(base_radius, cone_height)
    .lineTo(0, cone_height)
    .close()
    .revolve(360)
    .faces("+Z")
    .tag("base")
)

thin_shell = solid_cone.shell(-wall_thickness)

mount_radius = base_radius - wall_thickness - 5
hole_positions = [
    (mount_radius, 0),
    (0, mount_radius),
    (-mount_radius, 0),
    (0, -mount_radius),
]
part_with_holes = (
    thin_shell
    .faces("+Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

slot_box = (
    cq.Workplane("XY")
    .center(base_radius - wall_thickness - vent_slot_width / 2, cone_height - vent_slot_offset - vent_slot_height / 2)
    .box(vent_slot_width, vent_slot_height, wall_thickness * 2 + 0.2)
)

result = part_with_holes.cut(slot_box)

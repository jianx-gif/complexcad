import cadquery as cq

cavity_width = 80
cavity_length = 60
cavity_height = 15

dome_radius = 30
dome_cut_depth = 12

vent_slot_width = 20
vent_slot_height = 5
vent_slot_offset = 10

mount_hole_diameter = 5
mount_hole_offset = 8

rib_height = 5
rib_thickness = 3
rib_notch_width = 4
rib_notch_height = 2

chamfer_size = 1

base = cq.Workplane('XY').box(cavity_length, cavity_width, cavity_height, centered=True)
base = base.edges('|Z').chamfer(chamfer_size)

sphere = cq.Workplane('XY').sphere(dome_radius)
sphere = sphere.translate((0, 0, -cavity_height / 2 + dome_radius - dome_cut_depth))

cavity = base.cut(sphere)

vent = (
    cavity.faces('>Y')
    .workplane()
    .center(0, vent_slot_offset)
    .rect(vent_slot_width, vent_slot_height)
    .cutBlind(5)
)

px = cavity_length / 2 - mount_hole_offset - mount_hole_diameter / 2
py = cavity_width / 2 - mount_hole_offset - mount_hole_diameter / 2

with_holes = (
    vent.faces('<Z')
    .workplane()
    .pushPoints([
        (px, py),
        (-px, py),
        (-px, -py),
        (px, -py)
    ])
    .hole(mount_hole_diameter)
)

w = cavity_length - 2 * rib_thickness
h = rib_thickness
w_half = w / 2
h_half = h / 2
notch_w_half = rib_notch_width / 2
notch_h = rib_notch_height

rib = (
    cq.Workplane('XY')
    .center(0, -cavity_width / 4)
    .polyline([
        (-w_half, -h_half),
        (w_half, -h_half),
        (w_half, h_half),
        (notch_w_half, h_half),
        (notch_w_half, h_half + notch_h),
        (-notch_w_half, h_half + notch_h),
        (-notch_w_half, h_half),
        (-w_half, h_half)
    ])
    .close()
    .extrude(rib_height)
    .translate((0, 0, -cavity_height / 2 + rib_height / 2))
)

result = with_holes.union(rib)

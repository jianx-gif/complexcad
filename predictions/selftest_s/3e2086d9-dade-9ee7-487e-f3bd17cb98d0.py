import cadquery as cq
import math

outer_diameter = 80
hub_height = 60
shoulder_diameter = 50
shoulder_height = 15
base_thickness = 10
insert_diameter = 10
insert_length = 30
outer_chamfer = 2
mount_hole_diameter = 6
mount_hole_offset = 30
slot_width = 5
rib_count = 4
embed = 0.5

outer_radius = outer_diameter / 2.0
shoulder_radius = shoulder_diameter / 2.0
hub_cyl_height = hub_height - shoulder_height - base_thickness
shoulder_top_z = base_thickness + hub_cyl_height + shoulder_height

points = [
    (0, 0),
    (0, base_thickness),
    (outer_radius, base_thickness),
    (outer_radius, base_thickness + hub_cyl_height),
    (shoulder_radius, shoulder_top_z),
    (0, shoulder_top_z),
]

profile = cq.Workplane("XY").polyline(points).close()

hub = profile.revolve()

insert_cyl = cq.Workplane('XY').center(0, 0).circle(insert_diameter / 2).extrude(insert_length)
hub = hub.cut(insert_cyl).edges().chamfer(outer_chamfer)

slot_radial = outer_radius - shoulder_radius
slot_height = hub_cyl_height
slot = (
    cq.Workplane('XY')
    .box(slot_width, slot_radial, slot_height)
    .translate((shoulder_radius + slot_radial / 2, 0, base_thickness + hub_cyl_height / 2))
)

for i in range(rib_count):
    hub = hub.cut(slot.rotate((0, 0, 0), (0, 0, 1), i * (360 / rib_count)))

for i in range(rib_count):
    angle = i * (360 / rib_count)
    x = mount_hole_offset * math.cos(math.radians(angle))
    y = mount_hole_offset * math.sin(math.radians(angle))
    mount_hole = cq.Workplane('XY').center(x, y).circle(mount_hole_diameter / 2).extrude(base_thickness + 2)
    hub = hub.cut(mount_hole)

result = hub

import cadquery as cq

outer_diameter = 80.0
length = 50.0
wall_thickness = 4.0
neck_diameter = 40.0
neck_length = 20.0
taper_length = 5.0
vent_width = 12.0
vent_height = 4.0
vent_offset = 20.0
chamfer_size = 5.0
mount_hole_dia = 6.0
mount_hole_offset = 15.0
rib_width = 4.0
rib_height = 10.0
rib_depth = 2.0

outer_radius = outer_diameter / 2.0
neck_radius = neck_diameter / 2.0

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, length - neck_length - taper_length)
    .lineTo(outer_radius - taper_length, length - neck_length - taper_length)
    .lineTo(neck_radius, length - neck_length)
    .lineTo(neck_radius, length)
    .lineTo(0, length)
    .close()
)

solid_body = profile.revolve()

hollow = solid_body.shell(-wall_thickness)

vent_box = (
    cq.Workplane("XY")
    .box(vent_width, wall_thickness + 1.0, vent_height)
    .translate((outer_radius - wall_thickness / 2.0, 0, vent_offset))
)

with_vent = hollow.cut(vent_box)

mount_hole_cylinder = (
    cq.Workplane("XY")
    .circle(mount_hole_dia / 2.0)
    .extrude(wall_thickness + 2.0)
    .translate((outer_radius - wall_thickness / 2.0, 0, mount_hole_offset))
)

with_hole = with_vent.cut(mount_hole_cylinder)

rib_box = (
    cq.Workplane("XY")
    .box(rib_depth, rib_width, rib_height)
    .translate((outer_radius - rib_depth / 2.0, 0, length / 2.0))
)

with_rib = with_hole.union(rib_box)

result = with_rib.faces(">Z").edges().chamfer(chamfer_size)

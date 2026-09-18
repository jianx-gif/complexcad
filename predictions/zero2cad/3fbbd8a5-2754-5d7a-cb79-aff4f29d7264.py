import cadquery as cq

outer_diameter = 80.0
inner_diameter = 30.0
block_height = 60.0
base_thickness = 10.0
taper_angle = 5.0
chamfer_size = 2.0
mount_hole_diameter = 8.0
mount_hole_spacing = 40.0
rib_width = 8.0
rib_height = 15.0
rib_depth = 4.0
rib_count = 4
rib_spacing = 12.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, base_thickness)
    .lineTo(outer_radius, base_thickness)
    .lineTo(outer_radius, block_height)
    .lineTo(inner_radius, block_height)
    .close()
)

solid = profile.revolve()

solid = solid.faces("<Z").edges().chamfer(chamfer_size)

solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)

solid = (
    solid.faces(">Z")
    .workplane()
    .center(outer_radius - rib_width/2 - 5, 0)
    .rect(rib_width, rib_height)
    .cutBlind(-rib_depth)
)

result = solid
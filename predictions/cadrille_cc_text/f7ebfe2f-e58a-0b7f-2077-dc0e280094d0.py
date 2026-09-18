import cadquery as cq
leg_length = 80.0
leg_width = 60.0
thickness = 10.0
chamfer_distance = 6.0
central_hole_diameter = 8.0
mount_hole_diameter = 5.0
mount_hole_spacing = 20.0
mount_hole_edge_offset = 10.0
rib_height = 5.0
rib_thickness = 5.0
rib_spacing = 15.0
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_width, 0)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length + thickness)
    .lineTo(0, leg_length + thickness)
    .close()
)
base = base.edges("|Z").chamfer(chamfer_distance)
base = (
    base.faces(">Z")
    .workplane()
    .center(leg_width/2, leg_length/2)
    .hole(central_hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .center(leg_width/2, leg_length/2)
    .rect(rib_thickness, rib_height)
    .extrude(thickness)
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_distance)
mount_points = [
    (mount_hole_spacing/2, leg_length/2),
    (-mount_hole_spacing/2, leg_length/2),
    (mount_hole_spacing/2, leg_length/2),
    (-mount_hole_spacing/2, leg_length/2),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)
result = base

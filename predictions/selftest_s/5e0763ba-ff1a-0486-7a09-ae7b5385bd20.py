import cadquery as cq

arm_length = 80
base_width = 30
base_thickness = 12
end_width = 20
rib_width = 8
rib_height = 6
rib_offset = 2
rib_length = arm_length - 2 * rib_offset
rib_y_offset = (base_width - rib_width) / 2
hole_diameter = 6
hole_depth = 15
hole_position = arm_length * 0.6
hole_center_x = hole_position - arm_length / 2
chamfer_distance = 1
mount_hole_diameter = 4
mount_hole_offset = 10
mount_hole_edge_dist = 5
mount_hole_z = base_thickness - mount_hole_edge_dist - mount_hole_diameter / 2

main_body = (
    cq.Workplane("YZ")
    .rect(base_width, base_thickness, centered=False)
    .workplane(offset=arm_length)
    .rect(end_width, base_thickness, centered=False)
    .loft()
)

rib = (
    cq.Workplane("YZ")
    .rect(rib_width, rib_height, centered=False)
    .extrude(rib_length)
    .translate((rib_offset, rib_y_offset, rib_offset))
)

part = main_body.union(rib)

part = (
    part
    .faces(">Z")
    .workplane()
    .center(hole_center_x, 0)
    .hole(hole_diameter, depth=hole_depth)
)

mount_points = [
    (mount_hole_offset - arm_length / 2, mount_hole_z - base_thickness / 2),
    (arm_length - mount_hole_offset - arm_length / 2, mount_hole_z - base_thickness / 2)
]

part = (
    part
    .faces("<Y")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)

result = part.edges().chamfer(chamfer_distance)

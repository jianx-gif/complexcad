import cadquery as cq
arm_length = 80.0
base_width = 30.0
base_thickness = 12.0
rib_width = 8.0
rib_height = 6.0
rib_offset = 2.0
hole_diameter = 6.0
hole_depth = 15.0
hole_margin = 10.0
chamfer_distance = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(base_width, base_thickness)
    .extrude(base_width)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_thickness)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
rib = rib.translate((0, 0, base_thickness))
result = base.union(rib)
hole_positions = [
    (mount_hole_offset, 0),
    (-mount_hole_offset, 0),
    (0, mount_hole_offset),
    (0, -mount_hole_offset),
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .rect(rib_width, base_thickness)
    .extrude(rib_height)
)
result = result.edges("|Z").chamfer(chamfer_distance)

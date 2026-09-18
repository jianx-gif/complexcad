import cadquery as cq
arm_length = 80.0
arm_width = 30.0
arm_thickness = 10.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 4.0
rib_spacing = 15.0
rib_count = 4
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_width),
        (arm_length - arm_width, arm_width),
        (arm_length - arm_width, arm_width + arm_width),
        (arm_length - arm_width, arm_width + arm_width),
        (arm_length, arm_width),
        (0, arm_width),
        (0, 0)
    ])
    .close()
    .extrude(arm_thickness)
)
rib = (
    base.faces(">Z")
    .workplane()
    .center(0, arm_width / 2)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = rib.faces(">Z").workplane().center(0, arm_width / 2).rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces(">Z").workplane().center(0, arm_width / 2).rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces(">Z").workplane().center(0, arm_width / 2).rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.translate((0, arm_width / 2 - rib_thickness / 2, arm_thickness / 2))
rib = rib.translate((0, arm_width / 2 - rib_thickness / 2, arm_thickness / 2))
result = rib.union(rib)

import cadquery as cq
arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 4
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, arm_thickness))
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_distance)
hole_positions = [
    (-arm_length/2 + hole_offset, -arm_width/2 + hole_offset),
    (arm_length/2 - hole_offset, -arm_width/2 + hole_offset),
    (-arm_length/2 + hole_offset,  arm_width/2 - hole_offset),
    (arm_length/2 - hole_offset,  arm_width/2 - hole_offset),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.edges("|Z").chamfer(chamfer_distance)
result = base

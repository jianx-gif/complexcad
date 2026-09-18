import cadquery as cq
arm_length = 70
arm_width = 30
arm_thickness = 5
arm_height = 10
rib_width = 6
rib_height = 2
rib_spacing = 12
rib_count = 12
chamfer_size = 1
hole_diameter = 5
hole_spacing = 20
hole_offset = 10
base = cq.Workplane('XY').rect(arm_width, arm_length).extrude(arm_thickness)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.edges('|Z').chamfer(chamfer_size)
rib = (
    rib.faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, arm_thickness))
rib = rib.translate((0, 0, arm_thickness))
rib = rib.translate((0, 0, arm_thickness))
rib = rib.translate((0, 0, arm_thickness))
combined = base.union(rib)
hole_positions = [
    (arm_length/2 - hole_offset, arm_width/2 - hole_offset),
    (-arm_length/2 + hole_offset, arm_width/2 - hole_offset),
    (arm_length/2 - hole_offset, arm_width/2 - hole_offset),
    (-arm_length/2 + hole_offset, arm_width/2 - hole_offset)
]
result = (
    combined
    .faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

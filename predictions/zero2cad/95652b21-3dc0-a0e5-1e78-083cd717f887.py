import cadquery as cq

# Parameters
outer_diameter = 60.0
inner_diameter = 15.0
collar_thickness = 10.0
shoulder_length = 5.0
shoulder_diameter = 30.0
set_screw_diameter = 4.0
set_screw_head_diameter = 8.0
set_screw_head_depth = 2.0
chamfer_size = 0.5
slot_width = 4.0
slot_length = 12.0
slot_depth = 2.0

# Base collar profile and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, collar_thickness)
    .lineTo(outer_diameter / 2, collar_thickness)
    .lineTo(outer_diameter / 2, collar_thickness - shoulder_length)
    .lineTo(shoulder_diameter / 2, collar_thickness - shoulder_length)
    .lineTo(shoulder_diameter / 2, 0)
    .close()
)
base = profile.revolve()

# Central bore
bore = cq.Workplane("XY").circle(inner_diameter / 2).extrude(collar_thickness)
result = base.cut(bore)

# Set screw counterbore on side face
result = (
    result.faces(">X").first()
    .workplane()
    .center(0, collar_thickness / 2)
    .cboreHole(set_screw_diameter, set_screw_head_diameter, set_screw_head_depth)
)

# Slot on side face for access
result = (
    result.faces(">X").first()
    .workplane()
    .center(0, collar_thickness / 2)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)

# Chamfer all edges for safety
result = result.edges().chamfer(chamfer_size)

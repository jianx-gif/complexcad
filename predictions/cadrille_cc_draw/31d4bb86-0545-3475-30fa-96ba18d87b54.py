import cadquery as cq
arm_length = 80.0
arm_width = 40.0
arm_thickness = 15.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 3
rib_count = 4
rib_count = 6
rib_spacing = 15.0
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .cutBlind(-arm_thickness)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
combined = combined.union(rib)
result = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .cutBlind(-rib_width)
)

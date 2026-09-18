import cadquery as cq

arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
rib_height = 5.0
rib_width = 4.0
rib_spacing = 8.0
clearance_hole_diameter = 8.0
hole_offset_from_root = 15.0
chamfer_size = 0.5

rib_count = int((arm_length - rib_width) // rib_spacing) + 1

base = (
    cq.Workplane("YZ")
    .rect(arm_width, arm_thickness)
    .extrude(arm_length)
)

ribs = (
    base
    .faces(">Z")
    .workplane()
    .rect(rib_width, arm_width)
    .rarray(rib_spacing, 0, rib_count, 1, center=True)
    .extrude(rib_height)
)

combined = base.union(ribs)

hole_center_x = -arm_length/2 + hole_offset_from_root

with_hole = (
    combined
    .faces(">Z")
    .workplane()
    .center(hole_center_x, 0)
    .hole(clearance_hole_diameter)
)

result = with_hole.edges().chamfer(chamfer_size)

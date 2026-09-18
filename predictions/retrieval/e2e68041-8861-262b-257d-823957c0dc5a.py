import cadquery as cq

arm_length = 80.0
arm_width = 30.0
arm_thickness = 10.0
rib_width = 8.0
rib_height = 4.0
rib_offset = 15.0
fillet_radius = 2.0
hole_diameter = 5.0
hole_depth = 6.0
slot_width = 12.0
slot_depth = 3.0
slot_center_offset = 0.0
slot_cut_depth = 5.0

base = cq.Workplane("XY").box(arm_length, arm_width, arm_thickness)
base = base.edges("|Z").fillet(fillet_radius)

rib = base.faces(">Y").workplane().center(rib_offset, 0).rect(rib_width, arm_thickness).extrude(rib_height)

part = base.union(rib)

part = part.faces("<X").workplane().hole(hole_diameter, depth=hole_depth)

part = part.faces(">Z").workplane().center(slot_center_offset, 0).rect(slot_width, slot_depth).cutBlind(slot_cut_depth)

result = part
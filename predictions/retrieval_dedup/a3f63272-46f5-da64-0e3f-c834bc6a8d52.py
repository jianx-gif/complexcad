import cadquery as cq

flange_outer_diameter = 60.0
flange_thickness = 12.0
fillet_radius = 5.0
tap_diameter = 6.5
tap_depth = 10.0
shell_thickness = 2.0
edge_fillet = 0.5
slot_width = 10.0
slot_length = 20.0

base = (
    cq.Workplane("XY")
    .polygon(6, flange_outer_diameter)
    .center(flange_outer_diameter/2 - slot_width/2, 0)
    .rect(slot_width, slot_length)
    .extrude(flange_thickness)
)

filleted = base.edges("<<Z").fillet(fillet_radius)

hollow = filleted.shell(shell_thickness)

with_hole = hollow.faces(">Z").hole(tap_diameter, depth=tap_depth)

result = with_hole.edges("|Z").fillet(edge_fillet)

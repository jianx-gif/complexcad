import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 6.0
slot_width = 10.0
slot_length = 60.0
boss_diameter = 25.0
boss_height = 8.0
hole_diameter = 4.5
hole_spacing = 30.0
chamfer_size = 1.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Slot cut through the plate (centered on top edge)
slot = (
    base.faces(">Z")
    .workplane()
    .center(0, bracket_width/2 - slot_width/2)
    .rect(slot_length, slot_width)
    .cutBlind(-bracket_thickness)
)

# Central boss on the +X face
boss = (
    slot.faces(">X")
    .workplane()
    .center(0, 0)
    .circle(boss_diameter/2)
    .extrude(boss_height)
)

# Three M4 clearance holes on the top face, spaced along X axis
holes = (
    boss.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing, 0), (0, 0), (hole_spacing, 0)])
    .hole(hole_diameter)
)

# Apply chamfer to all outer edges
result = (
    holes.edges()
    .chamfer(chamfer_size)
)

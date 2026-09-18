import cadquery as cq

# Parameters
base_length = 80.0
base_height = 70.0
base_thickness = 10.0
fillet_radius = 2.0
chamfer_distance = 1.5
boss_diameter = 30.0
boss_height = 8.0
hole_diameter = 8.0
hole_spacing = 30.0
slot_width = 4.0
slot_length = 15.0
slot_offset = 10.0

# Triangular base sketch and extrusion
triangular_base = (
    cq.Workplane("XY")
    .polyline([
        (-base_length / 2, 0),
        (base_length / 2, 0),
        (0, base_height),
    ])
    .close()
    .extrude(base_thickness)
)

# Fillet vertical edges
triangular_base = triangular_base.edges("|Z").fillet(fillet_radius)

# Fillet top edges
triangular_base = triangular_base.edges(">Z").fillet(fillet_radius)

# Chamfer bottom edges
triangular_base = triangular_base.edges("<Z").chamfer(chamfer_distance)

# Central boss on top face
triangular_base = (
    triangular_base.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Three through holes on top face, centered horizontally
triangular_base = (
    triangular_base.faces(">Z")
    .workplane()
    .center(-hole_spacing, 0)
    .hole(hole_diameter)
    .center(hole_spacing * 2, 0)
    .hole(hole_diameter)
    .center(-hole_spacing, 0)
    .hole(hole_diameter)
)

# Slot cut on top face near left side
triangular_base = (
    triangular_base.faces(">Z")
    .workplane()
    .center(0, -slot_offset)
    .rect(slot_length, slot_width)
    .cutBlind(-base_thickness)
)

result = triangular_base
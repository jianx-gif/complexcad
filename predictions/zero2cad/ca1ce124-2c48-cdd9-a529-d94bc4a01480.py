import cadquery as cq

# Parameters
length = 80.0
height = 30.0
flange_width = 20.0
web_thickness = 5.0
flange_thickness = 8.0
fillet_radius = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 12.0
rib_depth = 2.0
rib_spacing = 15.0

# Base C‑channel profile
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (flange_width, 0),
        (flange_width, flange_thickness),
        (web_thickness, flange_thickness),
        (web_thickness, height - flange_thickness),
        (flange_width, height - flange_thickness),
        (flange_width, height),
        (0, height),
    ])
    .close()
)

# Extrude to length
result = profile.extrude(length)

# Fillet inner vertical edges (web‑flange junction)
result = result.edges("|Z").fillet(fillet_radius)

# Mounting holes on top flange (centered in web)
num_holes = int((length - 2 * hole_offset) // hole_spacing) + 1
hole_positions = [(hole_offset + i * hole_spacing, height - flange_thickness / 2) for i in range(num_holes)]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Stiffening ribs on top flange (cut pockets)
rib_count = int((length - 2 * hole_offset) // rib_spacing) + 1
rib_positions = [(hole_offset + i * rib_spacing, height - flange_thickness / 2) for i in range(rib_count)]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(rib_positions)
    .rect(rib_width, rib_height)
    .cutBlind(-rib_depth)
)

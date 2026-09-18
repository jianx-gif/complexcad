
import cadquery as cq

# Parameter definitions
base_length = 80.0
base_width = 50.0
base_thickness = 8.0
inner_cut_diameter = 30.0
boss_diameter = 20.0
boss_height = 12.0
hole_diameter = 4.0  # M4 hole
hole_radius_pattern = 22.0
chamfer_size = 1.5
rib_width = 8.0
rib_height = 6.0
rib_spacing = 20.0

# Base plate with inner cutout (non‑trivial sketch)
base_sketch = (
    cq.Sketch()
    .rect(base_length, base_width)
    .circle(inner_cut_diameter / 2, mode="s")
)

# Extrude base plate and apply chamfer on its vertical edges
base = (
    cq.Workplane("XY")
    .placeSketch(base_sketch)
    .extrude(base_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Add reinforcing ribs on the top surface (they will merge with the base)
rib_profile = (
    cq.Sketch()
    .rect(rib_width, base_length)
)

num_ribs = int((base_width - rib_width) // rib_spacing) + 1
rib_y_positions = [i * rib_spacing for i in range(num_ribs)]

base_with_ribs = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([(rib_width / 2, y) for y in rib_y_positions])
    .placeSketch(rib_profile)
    .extrude(rib_height)
)

# Central boss on the top surface
boss = (
    base_with_ribs
    .faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Drill central M4 hole through boss (through all material)
with_central_hole = (
    boss
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)

# Pattern of four additional M4 holes around the boss
hole_pattern = (
    with_central_hole
    .faces(">Z")
    .workplane()
    .polarArray(hole_radius_pattern, 0, 360, 4)
    .hole(hole_diameter)
)

result = hole_pattern

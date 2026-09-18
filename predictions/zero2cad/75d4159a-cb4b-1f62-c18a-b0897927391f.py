import cadquery as cq

# Parameters
bracket_width = 80.0
bracket_height = 40.0
bracket_thickness = 12.0
rib_width = 20.0
rib_height = 10.0
rib_thickness = 6.0
hole_diameter = 4.0
hole_spacing_x = 12.0
hole_spacing_y = 12.0
hole_rows = 3
hole_cols = 5
chamfer_distance = 1.0
boss_diameter = 12.0
boss_height = 5.0

# Base plate with chamfered outer edges
base = (
    cq.Workplane("XY")
    .box(bracket_width, bracket_thickness, bracket_height)
    .edges()
    .chamfer(chamfer_distance)
)

# Central rib on the back face (-Y)
rib = (
    base.faces("<Y")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

# Central boss on the front face (+Y)
boss = (
    base.faces(">Y")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Combine base, rib, and boss
combined = base.union(rib).union(boss)

# Patterned hole array on the front face (+Y)
result = (
    combined.faces(">Y")
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
    .hole(hole_diameter)
)

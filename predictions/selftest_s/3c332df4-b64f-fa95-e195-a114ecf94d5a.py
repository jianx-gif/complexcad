import cadquery as cq

# Parameters
outer_size = 40.0
wall_thickness = 2.0
conduit_length = 80.0
hole_diameter = 4.0
hole_spacing = 30.0
hole_rows = 2
hole_columns = 2
chamfer_size = 0.8
pattern_count = 3
pattern_spacing = 60.0

# Single conduit definition with chamfer before shell
single_conduit = (
    cq.Workplane("XY")
    .rect(outer_size, outer_size)
    .extrude(conduit_length)
    .edges()
    .chamfer(chamfer_size)
    .shell(-wall_thickness)
)

# Pattern duplicate conduits along X axis (still separate solids)
patterned = single_conduit
for i in range(1, pattern_count):
    patterned = patterned.union(single_conduit.translate((i * pattern_spacing, 0, 0)))

# Create a connecting rail that spans across the conduits to unify into one solid
total_width = (pattern_count - 1) * pattern_spacing + outer_size
rail = (
    cq.Workplane("XY")
    .center(total_width / 2 - outer_size / 2, outer_size / 2 + wall_thickness / 2)
    .box(total_width, wall_thickness, conduit_length)
)

# Merge rail with patterned conduits
unified = patterned.union(rail)

# Add tapped holes on three orthogonal faces of the unified part
result = (
    unified
    .faces(">X")
    .workplane()
    .rarray(hole_spacing, hole_spacing, hole_columns, hole_rows)
    .hole(hole_diameter)
    .faces("<X")
    .workplane()
    .rarray(hole_spacing, hole_spacing, hole_columns, hole_rows)
    .hole(hole_diameter)
    .faces(">Y")
    .workplane()
    .rarray(hole_spacing, hole_spacing, hole_columns, hole_rows)
    .hole(hole_diameter)
)

import cadquery as cq
import math

knob_outer_radius = 30.0
knob_height = 55.0
wall_thickness = 3.0
boss_radius = 8.0
boss_height = 12.0
fillet_radius = 2.0
chamfer_distance = 1.0
pocket_radius = 2.0
pocket_depth = 5.0
pocket_rows = 3
pocket_cols = 6
pocket_spacing_x = 8.0
pocket_spacing_y = 8.0

outer_profile = (
    cq.Workplane("XZ")
    .lineTo(0, knob_height * 0.4)
    .lineTo(knob_outer_radius - wall_thickness, knob_height * 0.4)
    .threePointArc(
        (knob_outer_radius - wall_thickness + 5, knob_height * 0.65),
        (knob_outer_radius - wall_thickness, knob_height - boss_height),
    )
    .lineTo(0, knob_height - boss_height)
    .close()
)

outer_solid = outer_profile.revolve()

hollow_knob = outer_solid.shell(wall_thickness)

# Create central boss by extruding from the bottom face so it fuses with the shell
boss = (
    hollow_knob.faces("<Z")
    .workplane()
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)

base_part = hollow_knob.union(boss)

# Patterned texture on the top face (>Z)
textured = (
    base_part.faces(">Z")
    .workplane()
    .center(0, 0)
    .rarray(pocket_spacing_x, pocket_spacing_y, pocket_cols, pocket_rows)
    .circle(pocket_radius)
    .cutBlind(-pocket_depth)
)

# Chamfer the bottom perimeter for safety
chamfered = textured.faces("<Z").edges().chamfer(chamfer_distance)

# Fillet the mounting (bottom) face edges for deburring
filleted = chamfered.faces("<Z").edges().fillet(fillet_radius)

result = filleted
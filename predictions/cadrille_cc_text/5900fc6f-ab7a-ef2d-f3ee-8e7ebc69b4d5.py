import cadquery as cq
lever_length = 80.0
tri_height = 20.0
boss_radius = 8.0
boss_length = 20.0
chamfer_len = 2.0
bolt_diameter = 5.0
bolt_counterbore_dia = 9.0
bolt_counterbore_depth = 5.0
hole_offset = 10.0
slot_width = 6.0
slot_length = 30.0
slot_count = 4
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (0, lever_length),
        (boss_radius, lever_length),
        (boss_radius, boss_length),
        (boss_radius, boss_length),
        (0, boss_length)
    ])
    .close()
    .extrude(tr厉害_length)
)
base = base.edges("|Z").chamfer(chamfer_len)
base = (
    base.faces(">Z")
    .workplane()
    .center(boss_radius - boss_length/2, 0)
    .hole(bolt_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(boss_radius - boss_length/2, 0)
    .hole(bolt_counterbore_dia)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(boss_radius - boss_length/2, 0)
    .hole(bolt_counterbore_dia, bolt_counterbore_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(boss_radius - boss_length/2, 0)
    .hole(bolt_counterbore_dia, bolt_counterbore_depth)
)
base = base.edges("|Z").chamfer(chamfer_len)
result = base

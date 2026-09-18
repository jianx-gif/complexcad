import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
boss_chamfer = 1.0
boss_chamfer = 0.5
blind_hole_dia = 5.0
blind_hole_depth = 4.0
hole_offset = 12.0
hole_count = 6
edge_chamfer = 0.5
rib_width = 8.0
rib_thickness = 3.0
rib_height = 2.0
rib_spacing = 15.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
boss = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .circle(boss_chamfer)
    .extrude(boss_chamfer)
)
result = base.union(boss)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .hole(blind_hole_dia, blind_hole_depth)
)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .hole(blind_hole_dia, blind_hole_depth)
)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .hole(blind_hole_dia, blind_hole_depth)
)

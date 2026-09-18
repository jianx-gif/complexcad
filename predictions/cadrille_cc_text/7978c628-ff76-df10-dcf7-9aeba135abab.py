import cadquery as cq
overall_width = 80.0
overall_height = 60.0
bracket_thickness = 8.0
leg_thickness = 12.0
leg_extension = 10.0
inner_fillet_radius = 3.0
outer_chamfer = 0.5
hole_diameter = 6.0
hole_counterbore_depth = 4.0
hole_tip_angle = 82.0
rib_height = 5.0
rib_thickness = 2.0
rib_length = overall_width - 2 * leg_extension
base = (
    cq.Workplane("XY")
    .rect(overall_width, overall_height)
    .extrude(bracket_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(leg_extension, leg_thickness)
    .cutBlind(-leg_extension)
)
hole_positions = [
    (-hole_tip_angle, -hole_tip_angle),
    (hole_tip_angle, -hole_tip_angle),
    (-hole_tip_angle, hole_tip_angle),
    (hole_tip_angle, hole_tip_angle),
]
base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, hole_counterbore_depth, hole_counterbore_depth)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, hole_counterbore_depth, hole_counterbore_depth)
)
rib = (
    base
    .faces(">Z")
    .workplane()
    .rect(rib_thickness, rib_length)
    .extrude(rib_height)
)
result = base.union(rib)

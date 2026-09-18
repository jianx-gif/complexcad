import cadquery as cq

clamp_length = 80.0
clamp_height = 30.0
flange_width = 60.0
flange_thickness = 10.0
web_thickness = 8.0
boss_diameter = 30.0
boss_height = 12.0
mount_hole_diameter = 6.0
fillet_radius = 4.0
edge_margin = 4.0

web_height = clamp_height - 2 * flange_thickness

half_flange = flange_width / 2.0
half_web = web_thickness / 2.0

profile = (
    cq.Sketch()
    .polygon(
        [
            (-half_flange, 0),
            (half_flange, 0),
            (half_flange, flange_thickness),
            (half_web, flange_thickness),
            (half_web, flange_thickness + web_height),
            (half_flange, flange_thickness + web_height),
            (half_flange, clamp_height),
            (-half_flange, clamp_height),
            (-half_flange, flange_thickness + web_height),
            (-half_web, flange_thickness + web_height),
            (-half_web, flange_thickness),
            (-half_flange, flange_thickness),
        ]
    )
)

body = (
    cq.Workplane("XY")
    .add(profile)
    .extrude(clamp_length)
)

boss = (
    body.faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
)

hole_x_spacing = clamp_length / 2.0 - edge_margin
hole_y_spacing = web_thickness / 2.0 - edge_margin
hole_positions = [
    (-hole_x_spacing / 2.0, -hole_y_spacing / 2.0),
    (-hole_x_spacing / 2.0, hole_y_spacing / 2.0),
    (hole_x_spacing / 2.0, -hole_y_spacing / 2.0),
    (hole_x_spacing / 2.0, hole_y_spacing / 2.0),
]

with_holes = (
    boss.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

result = (
    with_holes.edges("|Z and >Y")
    .fillet(fillet_radius)
)

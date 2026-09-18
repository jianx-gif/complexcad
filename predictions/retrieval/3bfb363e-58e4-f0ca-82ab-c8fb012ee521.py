import cadquery as cq

leg_length_a = 60.0
leg_length_b = 40.0
leg_thickness = 10.0
bracket_depth = 12.0
fillet_radius = 1.0
chamfer_size = 0.8
hole_diameter = 5.0
hole_offset = 8.0
hole_spacing = 20.0
rib_width = 6.0
rib_height = 8.0
pocket_width = 15.0
pocket_depth = 6.0

horizontal_hole_points = []
x = hole_offset
while x <= leg_length_a - hole_offset:
    horizontal_hole_points.append((x, leg_thickness/2))
    x += hole_spacing

vertical_hole_points = []
y = hole_offset
while y <= leg_length_b - hole_offset:
    vertical_hole_points.append((leg_thickness/2, y))
    y += hole_spacing

profile_points = [
    (0, 0),
    (leg_length_a, 0),
    (leg_length_a, leg_thickness),
    (leg_thickness, leg_thickness),
    (leg_thickness, leg_length_b),
    (0, leg_length_b),
]

result = (
    cq.Workplane("XY")
    .polyline(profile_points)
    .close()
    .extrude(bracket_depth)
    .edges("|X or |Y")
    .chamfer(chamfer_size)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .pushPoints(horizontal_hole_points)
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .pushPoints(vertical_hole_points)
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .center(leg_thickness/2, leg_thickness/2)
    .rect(rib_width, rib_width)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .center((leg_length_a - pocket_width)/2, leg_thickness/2)
    .rect(pocket_width, pocket_depth)
    .cutBlind(-bracket_depth/2)
)

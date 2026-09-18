import cadquery as cq

total_height = 50.0
base_outer_radius = 30.0
shoulder_outer_radius = 20.0
shoulder_height = 8.0
central_bore_diameter = 12.0
countersink_hole_diameter = 6.0
countersink_csk_diameter = 10.0
countersink_angle = 82.0
countersink_spacing = 30.0
top_chamfer = 0.8

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_outer_radius, 0)
    .lineTo(base_outer_radius, total_height - shoulder_height)
    .lineTo(shoulder_outer_radius, total_height - shoulder_height)
    .lineTo(shoulder_outer_radius, total_height)
    .lineTo(0, total_height)
    .close()
)

solid = profile.revolve()

with_bore = solid.faces(">Y").first().workplane().hole(central_bore_diameter)

with_counters = (
    with_bore.faces(">Y").first().workplane()
    .pushPoints([(countersink_spacing/2, 0), (-countersink_spacing/2, 0)])
    .cskHole(countersink_hole_diameter, countersink_csk_diameter, countersink_angle)
)

result = with_counters.faces(">Y").first().edges().chamfer(top_chamfer)

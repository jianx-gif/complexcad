import cadquery as cq

cylinder_length = 60.0
outer_diameter = 30.0
outer_radius = outer_diameter / 2.0
central_bore_diameter = 10.0
central_bore_radius = central_bore_diameter / 2.0
profile_height = 20.0
profile_top_radius = 15.0
arc_control_x = 7.5
arc_control_y = 30.0
arc_top_y = 25.0
slot_depth = 5.0   # radial extension outward from cylinder surface
slot_height = 5.0  # axial height of slot
slot_count = 12
chamfer_distance = 1.0

profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(profile_top_radius, 0)
    .lineTo(profile_top_radius, profile_height)
    .threePointArc((arc_control_x, arc_control_y), (0, arc_top_y))
    .close()
)

cylinder = profile.revolve(360)

bore = cq.Workplane("XY").circle(central_bore_radius).extrude(cylinder_length)

cylinder = cylinder.cut(bore)

slot_sketch = (
    cq.Workplane("XY")
    .transformed(rotate=(90, 0, 0))
    .moveTo(outer_radius + slot_depth / 2.0, 0)
    .rect(slot_depth, slot_height)
    .polarArray(0, 0, 360, slot_count)
)

cylinder = cylinder.cut(slot_sketch.extrude(-cylinder_length))

result = cylinder.edges("|Z").chamfer(chamfer_distance)

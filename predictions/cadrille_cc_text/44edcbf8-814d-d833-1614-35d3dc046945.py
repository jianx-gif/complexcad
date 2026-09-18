import cadquery as cq
cap_height = 40.0
outer_dia = 30.0
wall_thk = 2.0
rib_height = 8.0
rib_thk = 2.0
rib_thk = 3.0
hole_dia = 5.0
hole_count = 6
hole_spacing = (cap_height - 2 * wall_thk) / (hole_count - 1)
chamfer_distance = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_dia / 2, 0)
    .lineTo(outer_dia / 2, cap_height - rib_height)
    .lineTo(outer_dia / 2, cap_height - rib_height)
    .lineTo(0, cap_height - rib_height)
    .close()
)
result = profile.revolve()
result = result.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .circle(rib_thk / 2)
    .extrude(rib_height)
    .translate((0, 0, cap_height - rib_height))
)
result = result.union(rib)
hole_positions = [
    (hole_spacing, 0),
    (-hole_spacing, 0),
    (0, hole_spacing),
    (hole_spacing, 0),
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_dia)
)

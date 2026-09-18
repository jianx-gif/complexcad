import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
flange_thickness = 10.0
rib_height = 5.0
rib_width = 8.0
hole_diameter = 4.0
hole_count = 6
hole_radius = outer_diameter/2 - 5.0
hole_radius = inner_diameter/2
hole_radius = hole_radius + 5.0
base = (
    cq.Workplane("XZ")
    .moveTo(outer_diameter/2, 0)
    .lineTo(outer_diameter/2, flange_thickness)
    .lineTo(inner_diameter/2, flange_thickness)
    .lineTo(inner_diameter/2, 0)
    .close()
    .revolve(360)
)
rib = (
    cq.Workplane("XY")
    .circle(rib_width)
    .circle(rib_height)
    .extrude(rib_width)
)
result = base.union(rib)
hole_positions = [
    (hole_radius, 0),
    (-hole_radius, 0),
    (0, hole_radius),
    (hole_radius, 0),
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

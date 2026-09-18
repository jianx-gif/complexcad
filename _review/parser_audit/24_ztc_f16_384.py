import cadquery as cq

bracket_height = 40
outer_radius = 30
wall_thickness = 8
offset_distance = 2
fillet_radius = 2
hole_diameter = 12
hole_center_radius = wall_thickness/2 + offset_distance/2
hole_center_z = bracket_height * 0.6
rib_width = wall_thickness * 0.5
rib_height = bracket_height * 0.2
rib_z = bracket_height * 0.3

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .threePointArc((outer_radius + 10, bracket_height * 0.5), (outer_radius, bracket_height))
    .lineTo(0, bracket_height)
    .close()
    .offset2D(-wall_thickness)
)

bracket = profile.revolve()

bracket = bracket.edges().fillet(fillet_radius)

hole_cut = (
    cq.Workplane("XZ")
    .center(hole_center_radius, hole_center_z)
    .circle(hole_diameter / 2)
    .extrude(outer_radius * 2)
)
bracket = bracket.cut(hole_cut)

rib = (
    cq.Workplane("XZ")
    .center(wall_thickness - rib_width / 2, rib_z)
    .rect(rib_width, rib_height)
    .extrude(outer_radius * 2)
)
bracket = bracket.union(rib)

result = bracket

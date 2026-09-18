import cadquery as cq
outer_major_diameter = 80.0
outer_minor_diameter = 50.0
wall_thickness = 1.0
half_width = outer_major_diameter/2.0
half_height = outer_minor_diameter/2.0
cap_radius = half_height*0.8
profile = (
    cq.Workplane('XZ')
    .moveTo(0, -half_height)
    .lineTo(half_width - cap_radius, -half_height)
    .threePointArc((half_width, -half_height), (half_width, -half_height + cap_radius))
    .lineTo(half_width, half_height - cap_radius)
    .threePointArc((half_width, half_height), (half_width - cap_radius, half_height))
    .lineTo(0, half_height)
    .close()
)
solid = profile.revolve()

hollow = solid.shell(-wall_thickness)

flange = (
    cq.Workplane('XZ')
    .center(0, half_height)
    .circle(half_width + 6.0)
    .extrude(2.0)
)

part = hollow.union(flange)
result = part
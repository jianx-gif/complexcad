import cadquery as cq
# Parameters
pin_length = 80.0
pin_radius = 7.5
head_radius = 15.0
head_length = 12.0
bore_diameter = 6.0
chamfer_distance = 2.0
transition_fillet = 1.0
# Build half-profile for revolve
half_profile = (
    cq.Workplane('YZ')
    .moveTo(0, 0)
    .lineTo(pin_radius, 0)
    .lineTo(pin_radius, pin_length - head_length - transition_fillet)
    .threePointArc((head_radius, pin_length - head_length - transition_fillet + 2), (head_radius, pin_length - head_length))
    .lineTo(head_radius, pin_length)
    .lineTo(0, pin_length)
    .close()
)
# Revolve to create solid
solid = half_profile.revolve()
# Central bore
solid = solid.faces('>Z').workplane().hole(bore_diameter)
# Chamfer tip
solid = solid.edges('<Z').chamfer(chamfer_distance)
result = solid
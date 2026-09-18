import cadquery as cq
corner_radius = 20
wall_thickness = 5
height = 40
transition_length = 15
outer_radius = corner_radius + wall_thickness
pilot_hole_diameter = 4
pilot_hole_height = height / 2
chamfer_size = 1
rib_width = wall_thickness * 0.6
rib_height = height * 0.8
rib_depth = wall_thickness * 0.5
profile = (
    cq.Workplane("XY")
    .moveTo(corner_radius, 0)
    .lineTo(corner_radius, height - transition_length)
    .threePointArc((corner_radius + transition_length, height - transition_length), (corner_radius + transition_length, height))
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, 0)
    .close()
)
base_solid = profile.revolve()
rib_solid = (
    cq.Workplane('XY')
    .box(rib_depth, rib_width, rib_height, centered=False)
    .translate((corner_radius, 0, (height - rib_height) / 2))
)
combined = base_solid.union(rib_solid)
combined = combined.faces('>X').workplane().center(0, pilot_hole_height).hole(pilot_hole_diameter)
result = combined.edges('|Z').first().chamfer(chamfer_size)

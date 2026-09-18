import cadquery as cq

# Parameters
channel_height = 80.0
inner_radius_bottom = 15.0
outer_radius_top = 30.0
wall_thickness = 2.0
base_fillet_radius = 3.0
hole_diameter = 5.0
hole_count = 6
hole_axial_offset = 40.0
hole_radius_position = inner_radius_bottom + wall_thickness / 2

# Build profile
profile = (
    cq.Workplane('XZ')
    .moveTo(inner_radius_bottom, 0)
    .lineTo(inner_radius_bottom, 10)
    .threePointArc((inner_radius_bottom + 5, 15), (inner_radius_bottom + 5, 20))
    .lineTo(outer_radius_top, channel_height)
    .lineTo(outer_radius_top, 0)
    .close()
)

# Revolve, shell, fillet base, add radial holes
result = (
    profile
    .revolve()
    .shell(-wall_thickness)
    .faces('<Z')
    .edges()
    .fillet(base_fillet_radius)
    .workplane(offset=hole_axial_offset)
    .circle(hole_diameter / 2)
    .polarArray(radius=hole_radius_position, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter)
)

result
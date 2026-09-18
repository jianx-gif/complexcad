import cadquery as cq

# Parameters
cone_height = 80.0
base_radius = 40.0
wall_thickness = 2.0
hole_diameter = 5.0
hole_count = 12
hole_radius = base_radius - wall_thickness/2

# Create triangular profile and revolve
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(base_radius, cone_height)
    .lineTo(0, cone_height)
    .close()
)
solid = profile.revolve()

# Shell to create thin-walled cone
hollow = solid.shell(-wall_thickness)

# Add radial screw holes
result = (
    hollow
    .workplane()
    .polarArray(radius=hole_radius, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter)
)

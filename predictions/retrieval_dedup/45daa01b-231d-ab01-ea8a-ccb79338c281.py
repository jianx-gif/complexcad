import cadquery as cq
import math

# Dimensions
base_radius = 30.0
base_height = 10.0
shoulder_radius = 35.0
shoulder_height = 5.0
flange_radius = 45.0
flange_height = 8.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing_radius = 25.0

# Revolve solid
solid = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, base_height)
    .lineTo(shoulder_radius, base_height)
    .lineTo(shoulder_radius, base_height + shoulder_height)
    .lineTo(flange_radius, base_height + shoulder_height)
    .lineTo(flange_radius, base_height + shoulder_height + flange_height)
    .lineTo(0, base_height + shoulder_height + flange_height)
    .close()
    .revolve()
)

# Apply fillet to top outer edge
solid = solid.faces(">Z").edges().fillet(fillet_radius)
# Apply chamfer to base outer edge (bottom)
solid = solid.faces("<Z").edges().chamfer(chamfer_distance)

# Hole positions
outer_points = [
    (hole_spacing_radius * math.cos(theta), hole_spacing_radius * math.sin(theta))
    for theta in [0, math.pi/2, math.pi, 3*math.pi/2]
]
all_points = [(0, 0)] + outer_points

result = (
    solid.faces(">Z").workplane()
    .pushPoints(all_points)
    .hole(hole_diameter)
)

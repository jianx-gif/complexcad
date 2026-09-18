import cadquery as cq
import math

# Parameters
outer_diameter = 40.0
wall_thickness = 2.0
height = 20.0
inner_base_diameter = outer_diameter - 2 * wall_thickness
inner_top_diameter = 30.0
fillet_radius = 0.4
vent_hole_diameter = 6.0
side_hole_diameter = 4.0
side_hole_count = 3
rib_width = 2.0
rib_height = 4.0
rib_spacing_angle = 360 / side_hole_count

# Derived radii
outer_radius = outer_diameter / 2.0
inner_base_radius = inner_base_diameter / 2.0
inner_top_radius = inner_top_diameter / 2.0

# Outer solid
outer = cq.Workplane('XY').circle(outer_radius).extrude(height)

# Inner tapered solid via loft
inner = (
    cq.Workplane('XY')
    .circle(inner_base_radius)
    .workplane(offset=height)
    .circle(inner_top_radius)
    .loft()
)

# Hollow cap
cap = outer.cut(inner)

# Apply fillet to all edges (including inner surface edge)
cap = cap.edges().fillet(fillet_radius)

# Central vent hole through cap
cap = cap.faces('>Z').workplane().hole(vent_hole_diameter)

# Side mounting holes pattern around circumference
hole_radius = outer_radius - wall_thickness - 2.0
points = [
    (hole_radius * math.cos(math.radians(i * rib_spacing_angle)),
     hole_radius * math.sin(math.radians(i * rib_spacing_angle)))
    for i in range(side_hole_count)
]
cap = cap.faces('>Z').workplane().pushPoints(points).hole(side_hole_diameter)

# Add external ribs equally spaced around circumference
rib_profile = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
for i in range(side_hole_count):
    angle = i * rib_spacing_angle
    rib = rib_profile.translate((outer_radius - wall_thickness / 2.0, 0, height / 2.0))
    rib = rib.rotate((0, 0, 0), (0, 0, 1), angle)
    cap = cap.union(rib)

result = cap
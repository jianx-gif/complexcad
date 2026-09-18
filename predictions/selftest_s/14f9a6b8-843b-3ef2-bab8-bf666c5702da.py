import cadquery as cq
import math

hub_radius = 20.0
blade_length = 25.0
blade_height = 12.0
blade_thickness = 2.0
blade_span_angle = 30.0

tip_relief_depth = 1.5
tip_relief_length = 5.0
tip_relief_width = 6.0

chamfer_size = 0.5
hole_diameter = 3.0
hole_count = 3

blade_profile = (
    cq.Workplane("XZ")
    .moveTo(hub_radius, 0)
    .lineTo(hub_radius + blade_length, blade_height)
    .lineTo(hub_radius + blade_length - blade_thickness, blade_height)
    .lineTo(hub_radius, blade_thickness)
    .close()
)

blade = blade_profile.revolve(blade_span_angle)

relief_pocket = (
    cq.Workplane("XZ")
    .moveTo(
        hub_radius + blade_length - tip_relief_length / 2,
        blade_height - tip_relief_width / 2,
    )
    .rect(tip_relief_length, tip_relief_width)
    .extrude(tip_relief_depth)
)

blade_with_pocket = blade.cut(relief_pocket)

# Apply fillet to outer radial edges for safety
blade_fillet = blade_with_pocket.edges(">X").fillet(chamfer_size)

hole_cuts = None
for i in range(hole_count):
    angle = i * 2 * math.pi / hole_count
    x = (hub_radius - blade_thickness / 2) * math.cos(angle)
    y = (hub_radius - blade_thickness / 2) * math.sin(angle)
    cyl = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(hole_diameter / 2)
        .extrude(blade_height + 10)
    )
    hole_cuts = cyl if hole_cuts is None else hole_cuts.union(cyl)

result = blade_fillet.cut(hole_cuts)

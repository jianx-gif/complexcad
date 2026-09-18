import cadquery as cq
import math
from cadquery import selectors as sel

# Dimensions
outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
wall_thickness = 5.0
housing_length = 70.0
flange_diameter = 100.0
flange_radius = flange_diameter / 2.0
flange_thickness = 10.0
cavity_radius = 20.0
cavity_depth = 30.0
cavity_draft_angle = 5.0  # degrees
mounting_hole_diameter = 6.0
mounting_hole_edge = 10.0
rib_width = 5.0
rib_height = 3.0
rib_count = 3
chamfer_distance = 1.5

# Derived values
inner_radius = outer_radius - wall_thickness
draft_offset = math.tan(math.radians(cavity_draft_angle)) * cavity_depth
outer_top_radius = outer_radius - draft_offset
inner_top_radius = max(inner_radius - draft_offset, inner_radius * 0.5)

# Outer lofted shell body with draft
outer_body = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .workplane(offset=housing_length)
    .circle(outer_top_radius)
    .loft()
)

# Inner hollow loft
inner_body = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .workplane(offset=housing_length)
    .circle(inner_top_radius)
    .loft()
)

shell = outer_body.cut(inner_body)

# Mounting flange
flange = (
    cq.Workplane("XY")
    .cylinder(flange_thickness, flange_radius)
    .translate((0, 0, housing_length + flange_thickness / 2.0))
)
result = shell.union(flange)

# Recessed conical cavity (cut from interior)
conical_cavity = (
    cq.Workplane("XY")
    .add(cq.Solid.makeCone(cavity_radius, cavity_radius + draft_offset, cavity_depth))
    .translate((0, 0, cavity_depth / 2.0))
)
result = result.cut(conical_cavity)

# Internal ribs (protruding from inner wall above cavity depth)
for i in range(rib_count):
    z_position = cavity_depth + (i + 1) * (housing_length - cavity_depth) / (rib_count + 1)
    rib_length = housing_length / rib_count
    rib = (
        cq.Workplane("XY")
        .box(rib_width, rib_height, rib_length)
        .translate((inner_radius - rib_width / 2.0, 0, z_position))
    )
    result = result.union(rib)

# Chamfer bottom edge of shell for draft safety
result = result.edges(sel.NearestToPointSelector((0, 0, 0))).chamfer(chamfer_distance)

# Mounting holes on flange top face
hole_offset = flange_radius - mounting_hole_edge
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_offset, hole_offset),
        (-hole_offset, hole_offset),
        (-hole_offset, -hole_offset),
        (hole_offset, -hole_offset),
    ])
    .hole(mounting_hole_diameter)
)

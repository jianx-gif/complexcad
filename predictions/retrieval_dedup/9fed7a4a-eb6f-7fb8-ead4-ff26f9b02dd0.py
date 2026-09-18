import cadquery as cq
import math

outer_diameter = 80.0
height = 60.0
wall_thickness = 5.0
step_height = 20.0
step_inner_diameter = 40.0
fillet_radius = 3.0
base_thickness = 5.0
rib_height = 8.0
rib_width = 4.0
rib_count = 6
hole_diameter = 5.0
hole_pattern_radius = 30.0

outer_radius = outer_diameter / 2.0
step_inner_radius = step_inner_diameter / 2.0
inner_radius_base = outer_radius - wall_thickness

outer_cup = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
)

lower_frustum = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(inner_radius_base)
    .workplane(offset=step_height - base_thickness)
    .circle(step_inner_radius)
    .loft()
)

top_cylinder = (
    cq.Workplane("XY")
    .workplane(offset=step_height)
    .circle(step_inner_radius)
    .extrude(height - step_height)
)

interior_step = lower_frustum.union(top_cylinder)

cup_shell = outer_cup.cut(interior_step)

cup_fillet = cup_shell.edges().filter(lambda e: abs(e.Center().z - step_height) < 0.01).fillet(fillet_radius)

ribs = cq.Workplane("XY")
for i in range(rib_count):
    angle = i * 360.0 / rib_count
    ribs = ribs.union(
        cq.Workplane("XY")
        .center(outer_radius - rib_width / 2.0, 0)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .rect(rib_width, rib_height)
        .extrude(base_thickness)
    )

cup_with_ribs = cup_fillet.union(ribs)

hole_points = []
for i in range(rib_count):
    theta = math.radians(i * 360.0 / rib_count)
    x = hole_pattern_radius * math.cos(theta)
    y = hole_pattern_radius * math.sin(theta)
    hole_points.append((x, y))

result = (
    cup_with_ribs.faces("<Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)

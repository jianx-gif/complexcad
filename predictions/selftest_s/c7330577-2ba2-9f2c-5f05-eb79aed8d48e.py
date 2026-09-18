import cadquery as cq
import math

cap_outer_diameter = 60.0
cap_height = 40.0
wall_thickness = 4.0
rib_thickness = 2.0
rib_heights = [10.0, 20.0, 30.0]
hole_diameter = 3.0
hole_count = 6
hole_circle_radius = 15.0
chamfer_distance = 0.5

tab_width = 12.0
tab_height = 8.0
tab_depth = 5.0
boss_diameter = 10.0
boss_height = 6.0
pocket_diameter = 20.0
pocket_depth = 5.0

outer_radius = cap_outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

points = [
    (outer_radius, 0.0),
    (outer_radius, cap_height),
    (inner_radius, cap_height),
]

for h in sorted(rib_heights, reverse=True):
    points.append((inner_radius, h))
    points.append((inner_radius + rib_thickness, h))
    points.append((inner_radius, h))

points.append((inner_radius, 0.0))
points.append((outer_radius, 0.0))

profile = cq.Workplane("XZ").polyline(points).close()
solid = profile.revolve()

ang_step = 360.0 / hole_count
hole_pts = []
for i in range(hole_count):
    angle = i * ang_step
    x = hole_circle_radius * math.cos(math.radians(angle))
    y = hole_circle_radius * math.sin(math.radians(angle))
    hole_pts.append((x, y))

result = solid.faces(">Z").workplane().pushPoints(hole_pts).hole(hole_diameter)

boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    .translate((inner_radius, 0, 0))
)
result = result.union(boss)

result = result.faces(">Z").workplane().circle(pocket_diameter / 2).cutBlind(-pocket_depth)

tab = (
    cq.Workplane("XY")
    .box(tab_depth, tab_width, tab_height)
    .translate((outer_radius, 0, cap_height / 2))
)
result = result.union(tab)

result = result.faces(">Z").edges().chamfer(chamfer_distance)

import cadquery as cq
import math
max_diameter = 30
wall_thickness = 3
channel_radius = wall_thickness
spiral_turns = 3
spiral_start_radius = 5
spiral_end_radius = max_diameter/2 - wall_thickness
spiral_pitch = 10
total_height = spiral_turns * spiral_pitch
fillet_radius = 2
mount_hole_dia = 5
mount_hole_offset = max_diameter/2 - 5
mount_hole_count = 4
inlet_radius = 6
outlet_radius = 6
inlet_depth = 5
outlet_depth = 5
num_spiral_points = 150
points = []
for i in range(num_spiral_points + 1):
    t = i / num_spiral_points
    theta = t * spiral_turns * 2 * math.pi
    radius = spiral_start_radius + (spiral_end_radius - spiral_start_radius) * t
    x = radius * math.cos(theta)
    y = radius * math.sin(theta)
    z = t * total_height
    points.append((x, y, z))
path = cq.Workplane('XY').spline(points).wire()
channel = cq.Workplane('XY').circle(channel_radius).sweep(path, isFrenet=True)
outer_cyl = cq.Workplane('XY').cylinder(total_height + 10, max_diameter/2)
inlet_base = (
    cq.Workplane('XY')
    .workplane(offset=total_height/2 + 5)
    .circle(inlet_radius)
    .extrude(-inlet_depth)
)
inlet = inlet_base.edges('>Z').fillet(fillet_radius)
outlet_base = (
    cq.Workplane('XY')
    .workplane(offset=-total_height/2 - 5)
    .circle(outlet_radius)
    .extrude(outlet_depth)
)
outlet = outlet_base.edges('<Z').fillet(fillet_radius)
body = outer_cyl.cut(channel).cut(inlet).cut(outlet)
hole_cyl = cq.Workplane('XY').circle(mount_hole_dia/2).extrude(total_height + 10)
combined_holes = cq.Workplane('XY')
for i in range(mount_hole_count):
    angle = math.radians(i * 360 / mount_hole_count)
    x = mount_hole_offset * math.cos(angle)
    y = mount_hole_offset * math.sin(angle)
    combined_holes = combined_holes.union(hole_cyl.translate((x, y, -5)))
result = body.cut(combined_holes)

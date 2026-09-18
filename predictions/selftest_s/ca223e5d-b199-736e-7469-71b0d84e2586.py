import cadquery as cq
import math

# Parameters
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
pipe_height = 70.0
rib_width = 5.0
rib_start_ratio = 0.6
rib_start_z = pipe_height * rib_start_ratio
chamfer_distance = 0.5
hole_diameter = 5.0
hole_count = 4
hole_extra = 0.5
hole_length = wall_thickness + hole_extra

# Composite profile for revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rib_start_z)
    .lineTo(outer_radius + rib_width, rib_start_z)
    .lineTo(outer_radius + rib_width, pipe_height)
    .lineTo(outer_radius, pipe_height)
    .lineTo(inner_radius, pipe_height)
    .close()
)
solid_pipe = profile.revolve()

# Chamfer top and bottom outer edges
solid_pipe = solid_pipe.edges("(>Z or <Z)").chamfer(chamfer_distance)

# Create radial hole cylinder (axis will be aligned radially)
base_hole = (
    cq.Workplane("XY")
    .cylinder(hole_length, hole_diameter / 2)
    .rotate((0, 0, 0), (0, 1, 0), 90)
)

mid_radius = inner_radius + wall_thickness / 2
mid_z = pipe_height / 2
hole_cylinders = []
for i in range(hole_count):
    angle = math.radians(i * 360.0 / hole_count)
    x = mid_radius * math.cos(angle)
    y = mid_radius * math.sin(angle)
    hole_cylinders.append(base_hole.translate((x, y, mid_z)))

all_holes = hole_cylinders[0]
for h in hole_cylinders[1:]:
    all_holes = all_holes.union(h)

result = solid_pipe.cut(all_holes)

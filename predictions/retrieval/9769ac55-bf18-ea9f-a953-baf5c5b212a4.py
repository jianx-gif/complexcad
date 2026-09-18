import cadquery as cq
import math

outer_radius = 45.0
wall_thickness = 5.0
cover_height = 15.0
groove_width = 3.0
groove_depth = 2.0
boss_height = 5.0
hole_diameter = 3.0
hole_count = 4
hole_offset_angle = 0.0
chamfer_size = 0.5
intersect_offset = 0.5

inner_radius = outer_radius - wall_thickness
boss_radius = outer_radius - 0.5

profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, cover_height)
    .lineTo(inner_radius, cover_height)
    .lineTo(inner_radius, 0)
    .close()
)
base = profile.revolve()

boss = (
    cq.Workplane("XY")
    .cylinder(boss_height, boss_radius)
    .translate((0, 0, cover_height - intersect_offset + boss_height / 2.0))
)
base = base.union(boss)

groove = (
    cq.Workplane("XY")
    .cylinder(groove_depth, inner_radius + groove_width)
    .translate((0, 0, cover_height - groove_depth / 2.0))
)
base = base.cut(groove)

hole_radius = hole_diameter / 2.0
hole_cylinder = (
    cq.Workplane("XY")
    .cylinder(cover_height + 2.0, hole_radius)
    .translate((0, 0, (cover_height + 2.0) / 2.0))
)

for i in range(hole_count):
    angle = hole_offset_angle + i * 360.0 / hole_count
    x = (outer_radius - wall_thickness / 2.0) * math.cos(math.radians(angle))
    y = (outer_radius - wall_thickness / 2.0) * math.sin(math.radians(angle))
    base = base.cut(hole_cylinder.translate((x, y, 0)))

base = base.edges("|Z").chamfer(chamfer_size)

result = base
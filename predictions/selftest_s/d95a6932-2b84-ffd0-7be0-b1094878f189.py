import cadquery as cq
import math

outer_diameter = 80.0
wall_thickness = 2.0
channel_length = 100.0
hole_diameter = 4.0
countersink_diameter = 8.0
countersink_angle = 90.0
holes_per_ring = 8
num_rows = 3
chamfer_size = 0.5
notch_width = 4.0
notch_height = 10.0
rib_width = 6.0
rib_height = 12.0
rib_spacing = 25.0

inner_radius = outer_diameter/2 - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, channel_length)
    .lineTo(inner_radius + wall_thickness, channel_length)
    .lineTo(inner_radius + wall_thickness, 0)
    .close()
)
result = profile.revolve(360)
notch = (
    cq.Workplane("XZ")
    .moveTo(inner_radius + wall_thickness/2, channel_length/2)
    .rect(notch_width, notch_height)
    .extrude(wall_thickness*2)
)
result = result.cut(notch)
rib_base = (
    cq.Workplane("XZ")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness*2)
    .translate((inner_radius + wall_thickness/2, 0, 0))
)
rib_pattern = result
rib_count = int(channel_length / rib_spacing)
for i in range(rib_count):
    z_offset = (i + 0.5) * rib_spacing
    rib_instance = rib_base.translate((0, 0, z_offset))
    rib_pattern = rib_pattern.union(rib_instance)
result = rib_pattern
angle_rad = math.radians(countersink_angle)
cs_depth = (countersink_diameter - hole_diameter) / (2 * math.tan(angle_rad / 2))
for row in range(num_rows):
    z_offset = (row + 1) * (channel_length / (num_rows + 1))
    for i in range(holes_per_ring):
        theta = i * (360.0 / holes_per_ring) + ((row % 2) * (180.0 / holes_per_ring))
        rad = outer_diameter/2 - wall_thickness/2
        x = rad * math.cos(math.radians(theta))
        y = rad * math.sin(math.radians(theta))
        through = (
            cq.Workplane("XY")
            .circle(hole_diameter/2)
            .extrude(wall_thickness + cs_depth)
        )
        cone_solid = cq.Solid.makeCone(countersink_diameter/2, hole_diameter/2, cs_depth)
        sink = cq.Workplane("XY").add(cone_solid).translate((0, 0, wall_thickness + cs_depth))
        hole_solid = through.union(sink).translate((x, y, z_offset))
        result = result.cut(hole_solid)
# Chamfer end edges for safety
result = result.faces(">Z").edges().chamfer(chamfer_size)
result = result.faces("<Z").edges().chamfer(chamfer_size)


import cadquery as cq
import math

outer_diameter = 80.0
thickness = 5.0
fillet_radius = 2.0
hole_spacing = 12.0
hole_diameter_base = 4.0
hole_diameter_variation = 0.5
mount_hole_dia = 5.0
mount_offset = 10.0

base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
base = base.edges().fillet(fillet_radius)

r = outer_diameter/2 - hole_diameter_base/2 - 2.0
row = 0
while (row * hole_spacing) < (2 * r):
    y = -r + row * hole_spacing
    offset = (row % 2) * (hole_spacing/2)
    col = 0
    while (col * hole_spacing + offset) < (2 * r):
        x = -r + col * hole_spacing + offset
        if math.hypot(x, y) < r:
            dia = hole_diameter_base + ((row + col) % 2) * hole_diameter_variation
            base = base.faces('>Z').workplane().center(x, y).hole(dia)
        col += 1
    row += 1

for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    cx = (outer_diameter/2 - mount_offset) * math.cos(rad)
    cy = (outer_diameter/2 - mount_offset) * math.sin(rad)
    base = base.faces('>Z').workplane().center(cx, cy).hole(mount_hole_dia)

result = base

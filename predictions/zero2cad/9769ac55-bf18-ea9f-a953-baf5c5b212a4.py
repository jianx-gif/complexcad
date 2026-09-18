import cadquery as cq

outer_diameter = 80.0
wall_thickness = 5.0
cap_height = 15.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_rows = 3
hole_cols = 4
hole_offset = 6.0

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(cap_height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(cap_height - wall_thickness)
base = outer_cyl.cut(inner_cyl)

base = base.faces('<Z').edges().fillet(fillet_radius)

points = []
for row in range(hole_rows):
    y = (row - (hole_rows - 1) / 2.0) * hole_spacing
    x_offset = hole_offset if row % 2 else 0.0
    for col in range(hole_cols):
        x = (col - (hole_cols - 1) / 2.0) * hole_spacing + x_offset
        if (x**2 + y**2) <= (inner_radius - hole_diameter/2.0)**2:
            points.append((x, y))

result = base.faces('>Z').workplane().pushPoints(points).hole(hole_diameter)

result = result.faces('>Z').edges().chamfer(chamfer_distance)

import cadquery as cq

outer_radius = 40.0
inner_radius = 35.0
shell_height = 10.0
rim_height = 5.0
total_height = shell_height + rim_height
hole_diameter = 4.0
hole_spacing = 12.0
hole_rows = 3
hole_columns = 4
offset_half_spacing = hole_spacing / 2.0
chamfer_distance = 1.0
internal_fillet_radius = 2.0

outer = cq.Workplane('XY').circle(outer_radius).extrude(total_height)
inner = cq.Workplane('XY').circle(inner_radius).extrude(shell_height)
result = outer.cut(inner)

points = []
for i in range(hole_rows):
    for j in range(hole_columns):
        x = (j - (hole_columns - 1) / 2.0) * hole_spacing
        y = (i - (hole_rows - 1) / 2.0) * hole_spacing
        if i % 2 == 1:
            x += offset_half_spacing
        points.append((x, y))

result = result.faces('>Z').workplane().pushPoints(points).hole(hole_diameter)
result = result.faces('>Z').edges().chamfer(chamfer_distance)
result = result.faces('<Z').edges().fillet(internal_fillet_radius)

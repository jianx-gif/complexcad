import cadquery as cq
import math
outer_diameter = 80
wall_thickness = 8
housing_height = 60
central_bore_diameter = 20
counterbore_diameter = 30
counterbore_depth = 15
chamfer_size = 2
mount_hole_diameter = 5
mount_hole_count = 6
base_plate_margin = 10
base_plate_thickness = 5
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, housing_height)
    .lineTo(outer_radius, housing_height)
    .lineTo(outer_radius, 0)
    .close()
)
result = profile.revolve()
result = result.faces(">Z").workplane().hole(central_bore_diameter)
result = result.faces(">Z").workplane().circle(counterbore_diameter/2).cutBlind(counterbore_depth)
for i in range(mount_hole_count):
    angle = i * 360.0 / mount_hole_count
    x = (outer_radius - wall_thickness/2) * math.cos(math.radians(angle))
    y = (outer_radius - wall_thickness/2) * math.sin(math.radians(angle))
    hole = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(mount_hole_diameter/2)
        .extrude(housing_height + 2)
    )
    result = result.cut(hole)
base_plate = (
    result.faces("<Z").workplane()
    .rect(outer_diameter + 2*base_plate_margin, outer_diameter + 2*base_plate_margin)
    .extrude(base_plate_thickness)
)
result = result.union(base_plate)
result = result.edges("|Z").chamfer(chamfer_size)

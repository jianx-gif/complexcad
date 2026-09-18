import cadquery as cq

plate_radius = 35.0
plate_thickness = 8.0
rib_height = 3.0
rib_thickness = 2.0
hole_diameter = 5.0
hole_count = 12
hole_offset_radius = plate_radius - 8.0
fillet_radius = 0.6

base = (
    cq.Workplane("XZ")
    .moveTo(plate_radius, 0)
    .lineTo(plate_radius, plate_thickness)
    .lineTo(plate_radius + rib_height, plate_thickness)
    .lineTo(plate_radius + rib_height, plate_thickness + rib_thickness)
    .lineTo(plate_radius, plate_thickness + rib_thickness)
    .close()
    .revolve(360)
)

with_holes = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=hole_offset_radius, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter)
)

result = with_holes.edges().fillet(fillet_radius)

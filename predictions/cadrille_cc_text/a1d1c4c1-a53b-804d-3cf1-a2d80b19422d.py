import cadquery as cq
plate_radius = 35
plate_thickness = 8
fillet_radius = 0.6
rib_height = 3
rib_thickness = 2
hole_diameter = 5
hole_count = 6
hole_spacing = (plate_radius - rib_thickness) / 2
hole_positions = [(-plate_radius, 0), (plate_radius, 0)]
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(plate_radius, 0)
    .lineTo(plate_radius, plate_thickness)
    .lineTo(plate_radius - rib_thickness, plate_thickness)
    .lineTo(plate_radius - rib_thickness, plate_thickness + rib_height)
    .lineTo(0, plate_thickness + rib_height)
    .close()
    .revolve()
    .edges()
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
    .center(0, hole_spacing)
    .hole(hole_diameter)
)

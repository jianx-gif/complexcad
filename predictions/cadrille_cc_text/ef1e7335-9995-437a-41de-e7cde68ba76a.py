import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 6.0
rib_width = 30.0
rib_height = 12.0
hole_diameter = 10.0
hole_circle_radius = 20.0
chamfer_dist = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, plate_width)
    .extrude(rib_height)
)
rib = rib.edges("|Z").chamfer(chamfer_dist)
hole_positions = [
    (-plate_length/2 + hole_circle_radius, -plate_width/2 + hole_circle_radius),
    ( plate_length/2 - hole_circle_radius, -plate_width/2 + hole_circle_radius),
    (-plate_length/2 + hole_circle_radius,  plate_width/2 - hole_circle_radius),
    ( plate_length/2 - hole_circle_radius,  plate_width/2 - hole_circle_radius),
]
rib = (
    rib.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter/2)
    .cutBlind(-plate_thickness)
)
rib = rib.edges("|Z").chamfer(chamfer_dist)
result = rib

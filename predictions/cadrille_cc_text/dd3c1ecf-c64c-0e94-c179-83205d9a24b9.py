import cadquery as cq
plate_width = 80.0
plate_height = 60.0
plate_thickness = 5.0
hole_diameter = 5.0
countersink_diameter = 9.0
countersink_angle = 90.0
chamfer_dist = 1.0
rib_width = 6.0
rib_thickness = 2.0
rib_spacing = 20.0
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(plate_width - 2 * rib_width, plate_height - 2 * rib_width)
    .cutBlind(-plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, plate_height - 2 * rib_width)
    .extrude(rib_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, plate_thickness + rib_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, plate_thickness + rib_thickness)
)
rib = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, plate_height - 2 * rib_width)
    .extrude(rib_thickness)
)
result = base.union(rib)

import cadquery as cq

plate_width = 80.0
plate_height = 40.0
plate_thickness = 2.0
shelf_extension = 30.0
gusset_height = 20.0
gusset_thickness = 2.0
hole_diameter = 5.0
hole_offset_x = 25.0
hole_offset_y = 12.0
chamfer_dist = 0.5
notch_width = 10.0
notch_depth = 5.0
rib_height = 12.0
rib_thickness = 2.0
rib_offset_x = 15.0
rib_offset_y = 5.0

pts = [
    (0, 0),
    (plate_width, 0),
    (plate_width, plate_height),
    (plate_width - shelf_extension, plate_height),
    (plate_width - shelf_extension, plate_height - gusset_height),
    (plate_width - shelf_extension - gusset_thickness, plate_height - gusset_height),
    (plate_width - shelf_extension - gusset_thickness, plate_height),
    (0, plate_height),
    (0, 0)
]

base = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    .center(plate_width/2 - notch_width/2, -plate_thickness/2)
    .rect(notch_width, notch_depth)
    .cutBlind(-plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_dist)
)

rib = (
    cq.Workplane("XY")
    .rect(rib_thickness, rib_height)
    .extrude(plate_thickness)
    .translate((rib_offset_x, rib_offset_y, 0))
)

result = (
    base
    .union(rib)
    .workplane(offset=plate_thickness/2)
    .center(hole_offset_x, hole_offset_y)
    .hole(hole_diameter, depth=plate_thickness + 0.1)
)

import cadquery as cq
plate_width = 80.0
plate_height = 40.0
plate_thickness = 2.0
gusset_height = 20.0
gusset_thickness = 2.0
hole_diameter = 5.0
hole_offset_x = 25.0
hole_offset_y = 12.0
hole_offset_y = 12.0
chamfer_dist = 0.5
rib_height = 12.0
rib_thickness = 2.0
rib_offset_x = 15.0
rib_offset_y = 5.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (plate_width, 0),
        (plate_width, plate_height),
        (plate_width + notch_width, plate_height),
        (plate_width + notch_width, plate_height - notch_depth),
        (0, plate_height - notch_depth),
        (0, 0)
    ])
    .close()
    .extrude(plate_thickness)
)
gusset = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(gusset_thickness, gusset_height)
    .cutBlind(-gusset_thickness)
)
hole_positions = [
    (hole_offset_x, hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (-hole_offset_x, -hole_offset_y),
]
result = (
    hole_positions
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

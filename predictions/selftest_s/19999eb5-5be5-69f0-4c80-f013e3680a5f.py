import cadquery as cq

# Primary dimensions (max 100 units)
base_length = 80.0
base_width = 50.0
base_thickness = 8.0
wall_thickness = 1.0
fillet_radius = 3.0
chamfer_distance = 0.5
hinge_radius = 6.0
hinge_center_x = -20.0
hinge_center_y = 0.0
notch_width = 20.0
notch_height = 12.0
notch_offset_from_edge = 5.0
hole_diameter = 4.0
hole_spacing = 30.0
rib_height = 4.0
rib_width = 8.0
rib_length = base_length - 2 * wall_thickness
rib_spacing = 20.0

result = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
    .edges("|Z").fillet(fillet_radius)
    .edges("<Z").chamfer(chamfer_distance)
    .edges(">Z").chamfer(chamfer_distance)
    .faces("+Z")
    .workplane()
    .center(-base_length / 2 + notch_offset_from_edge + notch_width / 2, 0)
    .rect(notch_width, notch_height)
    .cutBlind(-base_thickness)
    .shell(wall_thickness)
    .faces(">Z[0]")
    .workplane()
    .center(hinge_center_x, hinge_center_y)
    .hole(hinge_radius * 2)
    .faces(">Z[0]")
    .workplane()
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    .hole(hole_diameter)
    .faces(">Z[0]")
    .workplane(offset=-rib_height)
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)

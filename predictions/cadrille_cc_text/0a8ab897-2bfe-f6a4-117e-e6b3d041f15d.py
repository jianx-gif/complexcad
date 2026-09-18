import cadquery as cq
jaw_length = 80.0
jaw_height = 20.0
jaw_thickness = 5.0
chamfer_angle_deg = 30.0
hole_diameter = 5.5
hole_spacing_x = 60.0
hole_spacing_y = 10.0
rib_height = 5.0
rib_thickness = 2.0
rib_length = jaw_length - 2 * rib_thickness
rib_length = jaw_length - 2 * rib_thickness
rib_start_x = jaw_length * 0.6
rib_end_y = jaw_height * 0.6
base = (
    cq.Workplane("XY")
    .rect(jaw_length, jaw_height)
    .extrude(jaw_thickness)
)
base = base.edges("|Z").chamfer(chamfer_angle_deg)
hole_positions = [
    (hole_spacing_x/2, hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2, -hole_spacing_y/2),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_length, rib_thickness)
    .extrude(rib_height)
)
rib = rib.translate((jaw_length/2 - rib_length/2, 0, jaw_thickness/2))
rib = rib.translate((jaw_length/2 - rib_length/2, 0, jaw_thickness/2))
result = base.union(rib)

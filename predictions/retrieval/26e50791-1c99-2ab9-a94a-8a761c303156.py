import cadquery as cq

outer_diameter = 70
wall_thickness = 4
cap_height = 20
flange_thickness = 6
flange_width = 10
rib_height = 6
rib_width = 8
lip_thickness = 1.5
lip_height = 2
chamfer_dist = 0.4

R_out = outer_diameter/2
R_in = R_out - wall_thickness

pts = [
    (0, 0),
    (R_out, 0),
    (R_out, cap_height - lip_height),
    (R_out + lip_thickness, cap_height - lip_height),
    (R_out + lip_thickness, cap_height),
    (R_out, cap_height),
    (R_in, cap_height),
    (R_in, rib_height),
    (R_in - rib_width, rib_height),
    (R_in - rib_width, 0),
    (0, 0)
]

profile = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve()
)

result = (
    profile
    .edges()
    .chamfer(chamfer_dist)
    .faces(">Z")
    .workplane()
    .rect(flange_width, flange_thickness)
    .cutBlind(-flange_thickness)
)

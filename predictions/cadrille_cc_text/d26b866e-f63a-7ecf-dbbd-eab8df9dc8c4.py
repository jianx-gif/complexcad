import cadquery as cq
flange_radius = 40.0
flange_thickness = 10.0
base_height = 30.0
base_width = 70.0
base_thickness = 8.0
pin_radius = 5.0
pin_length = 15.0
blind_hole_diameter = 6.0
blind_hole_depth = 6.0
chamfer_size = 2.0
mounting_hole_diameter = 4.0
mounting_hole_spacing = 30.0
rib_width = 5.0
rib_height = 3.0
rib_spacing = 15.0
base = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(base_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .rect(base_width, base_thickness)
    .extrude(base_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
base = (
    base.faces(">Z")
    .workplane()
    .circle(pin_radius)
    .extrude(base_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_thickness)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_size)
result = base

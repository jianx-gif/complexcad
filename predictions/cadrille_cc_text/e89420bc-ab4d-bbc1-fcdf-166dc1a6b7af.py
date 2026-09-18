import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 5.0
bolt_hole_diameter = 5.0
bolt_spacing_x = 50.0
bolt_spacing_y = 20.0
bolt_rows = 2
bolt_cols = 3
bolt_rows = 3
bolt_cols = 4
bolt_spacing_x = plate_length / bolt_spacing_y
bolt_spacing_y = bolt_spacing_y
rib_width = 5.0
rib_thickness = 3.0
rib_offset = 10.0
chamfer_size = 1.0
outer = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(plate_thickness)
)
outer = (
    outer
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
outer = outer.edges("|Z").chamfer(chamfer_size)
inner = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(bolt_hole_diameter / 2)
    .extrude(bolt_cols)
)
outer = outer.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_thickness)
    .extrude(rib_thickness)
)
result = outer.union(rib)

import cadquery as cq
plate_width = 80.0
plate_length = 60.0
plate_thickness = 50.0
outer_radius = 30.0
chamfer_size = 1.0
bolt_diameter = 5.0
bolt_count = 8
bolt_radius = outer_radius - 5.0
bolt_clearance = 1.0
bolt_clearance = 1.0
rib_width = 5.0
rib_height = 20.0
rib_thickness = 3.0
rib_count = 4
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .workplane(offset=plate_thickness)
    .rect(plate_width, plate_length)
    .loft()
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(plate_width - 2 * bolt_diameter, plate_length - 2 * bolt_diameter)
    .extrude(plate_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
rib = (
    base
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
result = base.union(rib)

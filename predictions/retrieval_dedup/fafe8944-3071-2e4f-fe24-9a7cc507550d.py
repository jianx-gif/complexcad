import cadquery as cq

outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 2.0
cavity_depth = 10.0
chamfer_size = 1.0
hole_diameter = 3.0
hole_spacing_y = 12.0
hole_spacing_z = 10.0
hole_rows = 2
hole_columns = 2
external_rib_length = 30.0
external_rib_height = 5.0
external_rib_thickness = 2.0

result = (
    cq.Workplane("XY")
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
    .faces(">Z or <Z")
    .shell(-wall_thickness)
    .faces(">Z")
    .workplane()
    .rect(outer_length - 2 * wall_thickness, outer_width - 2 * wall_thickness)
    .cutBlind(-cavity_depth)
    .edges("|Z")
    .chamfer(chamfer_size)
    .faces(">Y")
    .workplane()
    .rect(external_rib_length, external_rib_height)
    .extrude(external_rib_thickness, combine=True)
    .faces("<X")
    .workplane()
    .rarray(hole_spacing_y, hole_spacing_z, hole_rows, hole_columns)
    .hole(hole_diameter)
)

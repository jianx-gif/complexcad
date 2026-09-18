import cadquery as cq

outer_length = 80.0
outer_width = 50.0
outer_height = 25.0
wall_thickness = 1.5
rib_thickness = 2.0
rib_height = outer_height - 2 * wall_thickness - 2.0
chip_clearance_diameter = 12.0
chamfer_size = 0.8

interior_length = outer_length - 2 * wall_thickness
interior_width = outer_width - 2 * wall_thickness

result = (
    cq.Workplane("XY")
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
    .faces(">Z or <Z or >X or <X or >Y or <Y")
    .shell(-wall_thickness)
    .faces(">Z")
    .hole(chip_clearance_diameter)
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
    .faces("<Z")
    .workplane()
    .center(-interior_length / 4, 0)
    .rect(interior_width, rib_thickness)
    .extrude(rib_height)
    .mirror(mirrorPlane="YZ")
)

import cadquery as cq
outer_length = 80.0
outer_width = 50.0
outer_height = 25.0
wall_thickness = 1.5
rib_thickness = 2.0
rib_height = outer_height - 2 * wall_thickness
chip_clearance_diameter = 12.0
chamfer_size = 0.8
outer = (
    cq.Workplane("XY")
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
    .faces(">Z")
    .shell(-wall_thickness)
    .faces(">Z")
    .workplane()
    .rect(outer_length - 2 * wall_thickness, outer_width - 2 * wall_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (outer_length - 2 * wall_thickness - rib_thickness/2, 0),
        (outer_length - 2 * wall_thickness - rib_thickness/2, 0)
    ])
    .hole(rib_clearance_diameter)
)
rib = (
    cq.Workplane("XY")
    .box(outer_length - 2 * wall_thickness, outer_width - 2 * wall_thickness, rib_thickness)
    .translate((outer_length - wall_thickness - rib_thickness/2, 0, 0))
)
result = (
    rib
    .faces(">Z")
    .workplane()
    .pushPoints([
        (outer_length - wall_thickness - rib_thickness/2, 0),
        (outer_length - wall_thickness - rib_thickness/2, 0)
    ])
    .hole(2 * wall_clearance_diameter)
)

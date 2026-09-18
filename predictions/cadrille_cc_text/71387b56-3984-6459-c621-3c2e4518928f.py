import cadquery as cq
plate_width = 80.0
plate_depth = 30.0
plate_thickness = 5.0
web_thickness = 5.0
web_height = 12.0
hole_diameter = 5.0
hole_spacing_x = 20.0
hole_spacing_y = 15.0
chamfer = 1.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(web_thickness, web_height)
    .extrude(plate_thickness)
)
base = base.edges("|Z").chamfer(chamfer)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(web_thickness, plate_depth - 2 * web_height)
    .extrude(plate_thickness)
)
result = base

import cadquery as cq

base_width = 60.0
base_height = 30.0
base_thickness = 8.0
web_width = 12.0
web_height = 40.0
hole_diameter = 8.0
fillet_radius = 0.5
cut_depth = 2.0
cut_width = 4.0
cut_height = 2.0
cut_spacing_x = 12.0
cut_spacing_y = 12.0
cut_rows = 4
cut_cols = 2

hole_center_x = web_width / 2.0
hole_center_y = base_height + web_height / 2.0

base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(base_width, 0)
    .lineTo(base_width, base_height)
    .lineTo(web_width, base_height)
    .lineTo(web_width, base_height + web_height)
    .lineTo(0, base_height + web_height)
    .close()
    .extrude(base_thickness)
)

base = (
    base
    .faces(">Z")
    .workplane()
    .center(hole_center_x, hole_center_y)
    .hole(hole_diameter)
)

base = base.faces(">Z").edges().fillet(fillet_radius)

base = (
    base
    .faces(">Z")
    .workplane()
    .center(base_width / 2.0, base_height / 2.0)
    .rarray(cut_spacing_x, cut_spacing_y, cut_rows, cut_cols)
    .rect(cut_width, cut_height)
    .cutBlind(cut_depth)
)

result = base

import cadquery as cq
base_diameter = 60.0
base_thickness = 8.0
skirt_height = 20.0
skirt_thickness = 2.0
tab_width = 30.0
tab_height = 20.0
tab_thickness = 4.0
chamfer_dist = 0.5
tab_width = tab_width * 0.8
tab_height = 20.0
tab_thickness = 4.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_diameter / 2, 0)
    .lineTo(base_diameter / 2, base_thickness)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness + top_height)
    .lineTo(base_diameter / 2, base_thickness
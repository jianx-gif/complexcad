import cadquery as cq

# Parameters
base_diameter = 60.0
base_thickness = 8.0
skirt_height = 20.0
skirt_thickness = 2.0
tab_width = 30.0
tab_height = 20.0
tab_thickness = 4.0
chamfer_dist = 0.5

inner_radius = base_diameter / 2.0
outer_radius = inner_radius + skirt_thickness

top_z = base_thickness + skirt_height

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, base_thickness)
    .lineTo(outer_radius, base_thickness)
    .threePointArc((outer_radius + 5, base_thickness + skirt_height/2), (outer_radius, base_thickness + skirt_height))
    .lineTo(outer_radius, 0)
    .lineTo(inner_radius, 0)
    .close()
)

cup = profile.revolve()

offset_y = (inner_radius + outer_radius) / 2

tab = (
    cq.Workplane("XY")
    .rect(tab_width, tab_height)
    .extrude(tab_thickness)
    .translate((0, offset_y, top_z - tab_thickness/2))
)

result = (
    cup.union(tab)
    .edges()
    .chamfer(chamfer_dist)
)

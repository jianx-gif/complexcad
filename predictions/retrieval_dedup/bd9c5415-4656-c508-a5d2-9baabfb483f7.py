import cadquery as cq
panel_width = 80.0
panel_height = 50.0
panel_thickness = 5.0
hole_diameter = 9.0
countersink_diameter = 15.0
num_holes = 9
hole_spacing = 7.0
edge_fillet_radius = 1.0
rib_width = 10.0
rib_height = 30.0
rib_offset = 5.0
tab_width = 20.0
tab_height = 30.0
tab_thickness = 5.0
profile = (
    cq.Workplane("XY")
    .moveTo(-panel_width/2, -panel_height/2)
    .lineTo(panel_width/2 - 5, -panel_height/2)
    .threePointArc((panel_width/2, -panel_height/2), (panel_width/2, -panel_height/2 + 5))
    .lineTo(panel_width/2, panel_height/2 - 5)
    .threePointArc((panel_width/2, panel_height/2), (panel_width/2 - 5, panel_height/2))
    .lineTo(-panel_width/2, panel_height/2)
    .lineTo(-panel_width/2, -panel_height/2)
    .close()
    .extrude(panel_thickness)
)
rib = (
    profile.faces(">Z")
    .workplane()
    .center(0, rib_offset)
    .rect(rib_width, rib_height)
    .extrude(panel_thickness)
)
result = profile.union(rib)
# side tab on +X face
tab = (
    result.faces(">X")
    .workplane()
    .rect(tab_width, tab_height)
    .extrude(tab_thickness)
)
result = result.union(tab)
start_x = -((num_holes - 1) * hole_spacing) / 2
for i in range(num_holes):
    result = (
        result.faces(">Z")
        .workplane()
        .center(start_x + i*hole_spacing, 0)
        .cboreHole(hole_diameter, countersink_diameter, panel_thickness)
    )
# fillet outer edges on top face only
result = result.faces(">Z").edges().fillet(edge_fillet_radius)

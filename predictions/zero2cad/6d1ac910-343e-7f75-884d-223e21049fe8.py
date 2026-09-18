import cadquery as cq
panel_width = 80
panel_height = 60
panel_thickness = 3
corner_radius = 5
chamfer_size = 0.8
hole_diameter = 4
countersink_diameter = 7
countersink_angle = 45
hole_spacing = 12
hole_count = 5
hole_start_x = -panel_width/2 + 15
hole_y = 0
connector_hole_dia = 2.5
connector_spacing = 15
connector_rows = 2
connector_cols = 3
connector_start_x = -panel_width/2 + 20
connector_start_y = -panel_height/2 + 15
# base panel with rounded corner
base = (
    cq.Workplane("XY")
    .moveTo(-panel_width/2, -panel_height/2)
    .lineTo(panel_width/2 - corner_radius, -panel_height/2)
    .threePointArc((panel_width/2, -panel_height/2), (panel_width/2, -panel_height/2 + corner_radius))
    .lineTo(panel_width/2, panel_height/2)
    .lineTo(-panel_width/2, panel_height/2)
    .close()
    .extrude(panel_thickness)
)
# chamfer bottom edges
result = base.faces("<Z").edges().chamfer(chamfer_size)
# linear series of countersunk holes
for i in range(hole_count):
    x = hole_start_x + i * hole_spacing
    result = result.faces(">Z").workplane().center(x, hole_y).cskHole(hole_diameter, countersink_diameter, countersink_angle, panel_thickness)
# grid of connector holes
for r in range(connector_rows):
    for c in range(connector_cols):
        x = connector_start_x + c * connector_spacing
        y = connector_start_y + r * connector_spacing
        result = result.faces(">Z").workplane().center(x, y).hole(connector_hole_dia)
# rectangular pocket with a circular cutout
pocket_width = 30
pocket_height = 10
pocket_depth = 1.5
pocket_center_x = 0
pocket_center_y = panel_height/4
result = (
    result.faces(">Z").workplane()
    .center(pocket_center_x, pocket_center_y)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
result = (
    result.faces(">Z").workplane()
    .center(pocket_center_x, pocket_center_y)
    .circle(pocket_width/4)
    .cutBlind(-pocket_depth)
)

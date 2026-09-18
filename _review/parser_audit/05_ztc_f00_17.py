import cadquery as cq
# parameters
knob_length = 60.0
base_width = 40.0
base_height = 30.0
base_tab_width = 8.0
base_tab_height = 6.0
top_width = 30.0
top_height = 25.0
top_tab_width = 6.0
top_tab_height = 5.0
bottom_pts = [
    (-base_width/2, -base_height/2),
    ( base_width/2, -base_height/2),
    ( base_width/2, 0),
    ( base_width/2 + base_tab_width, 0),
    ( base_width/2 + base_tab_width, base_tab_height),
    ( base_width/2, base_tab_height),
    ( base_width/2, base_height/2),
    (-base_width/2, base_height/2),
    (-base_width/2, -base_height/2)
]

top_pts = [
    (-top_width/2, -top_height/2),
    ( top_width/2, -top_height/2),
    ( top_width/2, 0),
    ( top_width/2 + top_tab_width, 0),
    ( top_width/2 + top_tab_width, top_tab_height),
    ( top_width/2, top_tab_height),
    ( top_width/2, top_height/2),
    (-top_width/2, top_height/2),
    (-top_width/2, -top_height/2)
]
# base body via loft
body = (
    cq.Workplane('XZ')
    .polyline(bottom_pts).close()
    .workplane(offset=knob_length)
    .polyline(top_pts).close()
    .loft()
    .edges('|Z').chamfer(1.0)
)
# raised ridge for finger groove
ridge_width = 12.0
ridge_depth = 5.0
ridge_height = 8.0
ridge = (
    body.faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(ridge_width, ridge_depth)
    .extrude(ridge_height)
)
# combine body and ridge
combined = body.union(ridge)
# cut groove slot through ridge
groove_width = 6.0
groove_depth = 4.0
groove = (
    combined.faces('>Y')
    .workplane()
    .center(0, ridge_height/2)
    .rect(groove_width, ridge_height)
    .cutBlind(-groove_depth)
)
# counterbored hole on top face
hole_diameter = 5.0
counterbore_diameter = 9.0
counterbore_depth = 4.0
final_part = (
    groove.faces('>Z')
    .workplane()
    .cboreHole(hole_diameter, knob_length, counterbore_diameter, counterbore_depth)
)
result = final_part

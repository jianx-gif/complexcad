import cadquery as cq
inner_radius = 30.0
outer_radius = 40.0
height = 30.0
tab_width = 12.0
tab_height = 8.0
flex_cut_thickness = 2.0
flex_cut_depth = 2.0
hole_diameter = 3.0
hole_spacing = 8.0
hole_count = 8
chamfer = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, tab_height)
    .lineTo(inner_radius, tab_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer)
tab = (
    cq.Workplane("XY")
    .center(inner_radius + tab_height/2, 0)
    .rect(tab_width, tab_height)
    .extrude(tab_height)
)
solid = solid.union(tab)
hole_positions = [
    (hole_count-1.0, hole_count-1.0),
    (hole_count-1.0, hole_count-1.0),
    (hole_count+1.0, hole_count+1.0),
]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    solid.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(flex_cut_thickness, flex_cut_depth)
    .cutBlind(-flex_cut_depth)
)

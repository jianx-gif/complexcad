import cadquery as cq
panel_width = 80.0
panel_height = 60.0
panel_thickness = 4.0
corner_fillet_radius = 2.0
hole_diameter = 5.0
hole_spacing_x = 12.0
hole_spacing_y = 12.0
hole_rows = 2
hole_cols = 3
hole_margin = 10.0
slot_width = 30.0
slot_height = 5.0
slot_depth = panel_thickness
rib_thickness = 3.0
rib_width = 20.0
rib_length = 40.0
edge_hole_diameter = 3.0
edge_margin = 10.0
edge_offset = 5.0
base = (
    cq.Workplane("XY")
    .rect(panel_width, panel_height)
    .extrude(panel_thickness)
)
base = base.edges("|Z").fillet(corner_fillet_radius)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_height)
    .cutBlind(-panel_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_length)
    .extrude(rib_thickness)
)
base = base.union(rib)
base = base.edges("|Z").fillet(edge_margin)
base = base.edges("|Z").chamfer(edge_hole_diameter)
result = base

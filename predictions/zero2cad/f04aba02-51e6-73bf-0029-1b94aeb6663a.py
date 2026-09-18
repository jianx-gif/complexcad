import cadquery as cq

panel_width = 80.0
panel_height = 60.0
panel_thickness = 4.0
rib_width = 20.0
rib_height = 40.0
rib_thickness = 3.0
hole_diameter = 3.0
hole_spacing = 12.0
hole_count = 5
hole_row_y = -15.0
connector_hole_diameter = 5.0
connector_spacing = 10.0
connector_count = 4
connector_row_y = 10.0
slot_length = 30.0
slot_width = 5.0
slot_center_y = -20.0
fillet_radius = 2.0

result = cq.Workplane("XY").box(panel_width, panel_height, panel_thickness)
result = result.edges("|Z").fillet(fillet_radius)

rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, panel_thickness / 2))
)
result = result.union(rib)

result = (
    result.faces(">Z")
    .workplane()
    .center(-((hole_count - 1) * hole_spacing) / 2, hole_row_y)
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)

result = (
    result.faces(">Z")
    .workplane()
    .center(-((connector_count - 1) * connector_spacing) / 2, connector_row_y)
    .rarray(connector_spacing, 0, connector_count, 1)
    .hole(connector_hole_diameter)
)

result = (
    result.faces(">Z")
    .workplane()
    .center(0, slot_center_y)
    .rect(slot_length, slot_width)
    .cutThruAll()
)

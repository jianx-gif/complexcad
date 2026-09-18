import cadquery as cq

panel_width = 80.0
panel_height = 50.0
panel_thickness = 5.0
boss_height = 2.0
hole_diameter = 12.0
boss_diameter = 20.0
fillet_radius = 0.5
hole_spacing = 15.0
hole_count = 5
connector_hole_diameter = 6.0
connector_hole_spacing = 20.0
notch_width = 20.0
notch_height = 10.0
notch_depth = 5.0

profile = (
    cq.Workplane("XY")
    .moveTo(-panel_width/2, -panel_height/2)
    .lineTo(panel_width/2, -panel_height/2)
    .lineTo(panel_width/2, -panel_height/2 + notch_depth)
    .threePointArc(
        (panel_width/2 - notch_width/2, -panel_height/2 + notch_depth + notch_height/2),
        (panel_width/2 - notch_width, -panel_height/2 + notch_depth)
    )
    .lineTo(-panel_width/2, -panel_height/2 + notch_depth)
    .close()
)

base_panel = profile.extrude(panel_thickness)

boss_positions = [((-panel_width/2) + 15 + i*hole_spacing, 0) for i in range(hole_count)]

bosses = (
    base_panel.faces("<Z").workplane()
    .pushPoints(boss_positions)
    .circle(boss_diameter/2)
    .extrude(boss_height)
)

result = base_panel.union(bosses)

result = (
    result.faces(">Z").workplane()
    .pushPoints(boss_positions)
    .hole(hole_diameter, depth=panel_thickness + boss_height)
)

connector_positions = [((-panel_width/2) + 10 + i*connector_hole_spacing, -panel_height/2 + 10) for i in range(3)]
result = (
    result.faces(">Z").workplane(offset=panel_thickness/2)
    .pushPoints(connector_positions)
    .hole(connector_hole_diameter)
)

result = result.edges().fillet(fillet_radius)

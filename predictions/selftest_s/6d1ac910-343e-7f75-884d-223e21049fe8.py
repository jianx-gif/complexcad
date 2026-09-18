import cadquery as cq

panel_width = 100.0
panel_height = 70.0
panel_thickness = 4.0
corner_radius = 6.0
chamfer_dist = 1.0
hole_diameter = 4.0
countersink_diameter = 8.0
countersink_angle = 60.0
hole_rows = 2
hole_cols = 8
hole_row_spacing = 15.0
hole_col_spacing = 10.0
extra_hole_diameter = 3.0
extra_hole_spacing = 12.0
extra_hole_count = 4
extra_hole_offset_y = -20.0

half_w = panel_width / 2.0
half_h = panel_height / 2.0

# Base panel sketch with rounded top‑right corner and a central rectangular pocket
base = (
    cq.Workplane("XY")
    .moveTo(-half_w + corner_radius, -half_h)
    .lineTo(half_w - corner_radius, -half_h)
    .threePointArc((half_w, -half_h), (half_w, -half_h + corner_radius))
    .lineTo(half_w, half_h)
    .lineTo(-half_w, half_h)
    .close()
)

panel = base.extrude(panel_thickness)

# Add a centered rectangular pocket on the upper half of the panel
pocket_width = panel_width * 0.4
pocket_height = panel_height * 0.2
panel = (
    panel.workplane(offset=panel_thickness)
    .center(0, half_h * 0.5)
    .rect(pocket_width, pocket_height)
    .cutBlind(-panel_thickness * 0.6)
)

# Apply a small chamfer to all outer edges for safety
panel = panel.edges("<<Z").chamfer(chamfer_dist)

# Double line of countersink holes centered horizontally
start_x = -((hole_cols - 1) * hole_col_spacing) / 2.0
for col in range(hole_cols):
    x_pos = start_x + col * hole_col_spacing
    for row in range(hole_rows):
        y_offset = (row - 0.5) * hole_row_spacing
        panel = (
            panel.workplane(offset=panel_thickness / 2.0)
            .center(x_pos, y_offset)
            .cskHole(hole_diameter, countersink_diameter, countersink_angle, panel_thickness)
        )

# Linear array of through holes on the lower side for connectors
for i in range(extra_hole_count):
    x_pos = -((extra_hole_count - 1) * extra_hole_spacing) / 2.0 + i * extra_hole_spacing
    panel = (
        panel.workplane(offset=panel_thickness / 2.0)
        .center(x_pos, extra_hole_offset_y)
        .hole(extra_hole_diameter)
    )

result = panel
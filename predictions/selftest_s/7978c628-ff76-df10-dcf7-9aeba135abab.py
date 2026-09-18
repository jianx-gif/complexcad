import cadquery as cq

overall_width = 80.0
overall_height = 60.0
bracket_thickness = 8.0
leg_thickness = 12.0
inner_fillet_radius = 3.0
outer_chamfer = 0.5
hole_diameter = 6.0
hole_tip_angle = 82.0
hole_counterbore_depth = 4.0
rib_height = 5.0
rib_thickness = 2.0

# Base U‑shaped bracket by extruding outer rectangle and cutting inner void
result = cq.Workplane("XY").rect(overall_width, overall_height).extrude(bracket_thickness)
inner_gap_width = overall_width - 2 * leg_thickness
inner_gap_height = overall_height - leg_thickness
result = (
    result.faces(">Z")
    .workplane()
    .rect(inner_gap_width, inner_gap_height)
    .translate((0, -leg_thickness/2))
    .cutBlind(-bracket_thickness)
)

# Fillet inner and outer vertical edges, chamfer top perimeter
result = result.edges("|Z").fillet(inner_fillet_radius)
result = result.faces(">Z").edges().chamfer(outer_chamfer)

# Countersunk holes on each leg near the top
hole_x_offset = overall_width/2 - leg_thickness/2
hole_y_offset = overall_height/2 - leg_thickness/4
hole_positions = [(-hole_x_offset, hole_y_offset), (hole_x_offset, hole_y_offset)]
result = result.faces(">Z").workplane().pushPoints(hole_positions).cskHole(hole_diameter, hole_tip_angle, hole_counterbore_depth)

# Reinforcing rib on the back face
result = result.faces("<Y").workplane().center(0, 0).rect(overall_width/2, rib_height).extrude(rib_thickness)

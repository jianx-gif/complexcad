import cadquery as cq

# Parameters
body_length = 80.0
inlet_radius = 15.0
outlet_radius = 12.0
wall_thickness = 3.0
fillet_radius = 1.5
chamfer_distance = 0.8
mount_hole_diameter = 8.0
mount_hole_offset = 20.0
tab_width = 30.0
tab_height = 10.0
tab_thickness = 6.0

# Outer profile sketch on XY plane (X = radius, Y = axial)
outer_profile = (
    cq.Workplane("XY")
    .moveTo(inlet_radius, 0)
    .lineTo(inlet_radius, body_length * 0.2)
    .threePointArc((inlet_radius + 5, body_length * 0.3), (outlet_radius + 5, body_length * 0.5))
    .threePointArc((outlet_radius, body_length * 0.6), (outlet_radius, body_length * 0.8))
    .lineTo(outlet_radius, body_length)
    .close()
)

# Inner profile sketch (offset by wall thickness)
inner_profile = (
    cq.Workplane("XY")
    .moveTo(inlet_radius - wall_thickness, 0)
    .lineTo(inlet_radius - wall_thickness, body_length * 0.2)
    .threePointArc((inlet_radius - wall_thickness + 2, body_length * 0.3), (outlet_radius - wall_thickness - 2, body_length * 0.5))
    .threePointArc((outlet_radius - wall_thickness, body_length * 0.6), (outlet_radius - wall_thickness, body_length * 0.8))
    .lineTo(outlet_radius - wall_thickness, body_length)
    .close()
)

# Revolve profiles to create solids
outer_solid = outer_profile.revolve()
inner_solid = inner_profile.revolve()

# Subtract inner from outer to create hollow body
hollow_body = outer_solid.cut(inner_solid)

# Fillet inlet edge (bottom circular edge)
filleted_body = hollow_body.faces("<Y").edges().fillet(fillet_radius)

# Add mounting tab on inlet side (negative Y face)
with_tab = (
    filleted_body
    .faces("<Y")
    .workplane()
    .rect(tab_width, tab_thickness)
    .extrude(tab_height)
)

# Chamfer vertical edges of the tab for safety
chamfered_body = with_tab.edges("|Z").chamfer(chamfer_distance)

# Drill mounting hole through tab (centered on tab)
result = (
    chamfered_body
    .faces("<Y")
    .workplane()
    .center(0, mount_hole_offset)
    .hole(mount_hole_diameter)
)

import cadquery as cq

knob_outer_radius = 25.0
knob_height = 15.0
base_height = 3.0
base_fillet_radius = 2.0
shaft_radius = 6.0
shaft_height = 10.0
cup_radius = 12.0
cup_depth = 3.0
pocket_radius = 4.0
pocket_depth = 7.0

total_height = base_height + knob_height + shaft_height

# Create half-profile for revolve
profile = (
    cq.Workplane('YZ')
    .moveTo(0, 0)
    .lineTo(0, base_height)
    .threePointArc((base_fillet_radius, base_height + base_fillet_radius), (knob_outer_radius, base_fillet_radius + base_height))
    .lineTo(knob_outer_radius, base_height + knob_height)
    .lineTo(0, total_height)
    .close()
)

# Revolve profile to make knob body
knob_body = profile.revolve()

# Shallow cup cut (recess) on top of knob
cup_cut = (
    cq.Workplane('XY')
    .circle(cup_radius)
    .extrude(cup_depth)
    .translate((0, 0, base_height + knob_height - cup_depth/2))
)

# Blind pocket inside knob
pocket_cut = (
    cq.Workplane('XY')
    .circle(pocket_radius)
    .extrude(pocket_depth)
    .translate((0, 0, base_height + knob_height/2))
)

# Shaft extension
shaft = (
    cq.Workplane('XY')
    .circle(shaft_radius)
    .extrude(shaft_height)
    .translate((0, 0, base_height + knob_height))
)

# Combine features
result = knob_body.cut(cup_cut).cut(pocket_cut).union(shaft)

# Fillet at base edge
result = result.faces('<Z').edges().fillet(base_fillet_radius)

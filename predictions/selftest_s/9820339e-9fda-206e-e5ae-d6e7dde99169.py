import cadquery as cq

knob_outer_radius = 30.0
knob_height = 20.0
inner_shaft_radius = 8.0
rib_thickness = 2.0
rib_height = 5.0
keyway_width = 8.0
keyway_depth = 6.0
thread_diameter = 5.0
fillet_radius = 1.5
keyway_fillet = 0.8

base = (
    cq.Workplane('XY')
    .circle(knob_outer_radius)
    .extrude(knob_height)
    .tag('knob_base')
)

rib = (
    cq.Workplane('XY')
    .circle(knob_outer_radius - rib_thickness)
    .extrude(rib_height)
    .translate((0, 0, knob_height - rib_height))
)

result = base.union(rib)

keyway_cutter = (
    cq.Workplane('XZ')
    .center(knob_outer_radius - keyway_depth/2, knob_height/2)
    .rect(keyway_depth, knob_height)
    .extrude(keyway_width)
)

result = result.cut(keyway_cutter)

result = (
    result.faces('>Z')
    .workplane()
    .hole(thread_diameter)
)

result = result.edges('<<Z[-1]').fillet(fillet_radius)

result = result.faces('>X').edges().fillet(keyway_fillet)

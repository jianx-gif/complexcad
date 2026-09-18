import cadquery as cq
import math
knob_outer_radius = 30.0
knob_height = 20.0
inner_shaft_radius = 8.0
inner_shaft_radius = 1.5
keyway_fillet = 0.8
keyway_width = 8.0
keyway_depth = 6.0
thread_diameter = 5.0
fillet_radius = 1.5
rib_thickness = 2.0
rib_height = 5.0
base = (
    cq.Workplane("XY")
    .circle(knob_outer_radius)
    .extrude(knob_height)
)
base = base.edges().fillet(fillet_radius)
base = base.edges().fillet(fillet_radius)
base = base.faces(">Z").workplane().hole(thread_diameter)
base = base.faces(">Z").workplane().hole(thread_diameter)
base = base.faces(">Z").workplane().hole(thread_diameter)
base = base.faces("<Z").workplane().rect(keyway_width, keyway_depth).extrude(keyway_depth)
base = base.faces(">Z").workplane().circle(keyway_depth).extrude(keyway_depth)
base = base.faces(">Z").workplane().polarArray(radius=knob_outer_radius - rib_thickness/2, count=rib_thickness, startAngle=0, angle=360).rect(rib_thickness, rib_height).extrude(rib_thickness)
base = base.union(base)
base = base.faces(">Z").edges().fillet(fillet_radius)
base = base.faces(">Z").edges().fillet(fillet_radius)
base = base.faces(">Z").edges().fillet(fillet_radius)
result = base

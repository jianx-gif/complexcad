import cadquery as cq
import math

body_diameter = 60.0
body_length = 80.0
wall_thickness = 2.0
inlet_diameter = 15.0
outlet_diameter = 12.0
inlet_offset = 20.0
outlet_offset = 60.0
fillet_radius = 5.0
flange_diameter = 90.0
flange_thickness = 5.0
bolt_hole_diameter = 4.0
bolt_hole_count = 4
bolt_hole_radius = 40.0

body = (
    cq.Workplane("XY")
    .circle(body_diameter / 2)
    .extrude(body_length)
    .shell(-wall_thickness)
)

body = body.edges().fillet(fillet_radius)

inlet_cutter = (
    cq.Workplane("YZ")
    .center(0, inlet_offset)
    .circle(inlet_diameter / 2)
    .extrude(body_diameter + 2 * wall_thickness)
)

outlet_cutter = (
    cq.Workplane("YZ")
    .center(0, outlet_offset)
    .circle(outlet_diameter / 2)
    .extrude(body_diameter + 2 * wall_thickness)
)

body = body.cut(inlet_cutter).cut(outlet_cutter)

flange = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
    .translate((0, 0, -flange_thickness))
)

bolt_holes = (
    cq.Workplane("XY")
    .polarArray(bolt_hole_radius, 0, 360, bolt_hole_count)
    .circle(bolt_hole_diameter / 2)
    .extrude(flange_thickness + 2)
)

flange = flange.cut(bolt_holes)

result = body.union(flange)

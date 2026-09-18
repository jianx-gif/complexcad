import cadquery as cq
import math
total_height = 60.0
outer_radius_bottom = 30.0
outer_radius_top = 20.0
wall_thickness = 4.0
valve_cut_radius = 12.0
valve_cut_depth = 8.0
bolt_hole_dia = 5.0
bolt_pattern_radius = 22.0
bolt_head_dia = 9.0
bolt_head_angle = 90.0
chamfer_size = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius_bottom, 0)
    .lineTo(outer_radius_bottom, total_height - valve_cut_radius)
    .lineTo(outer_radius_top, total_height - valve_cut_radius)
    .lineTo(outer_radius_top, total_height)
    .lineTo(outer_radius_bottom, total_height)
    .lineTo(0, total_height)
    .close()
)
valve = profile.revolve()
valve = valve_cut_depth
valve = valve_cut_depth
valve = valve_cut_depth
valve = valve.cut(valve)
valve = (
    valve
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(bolt_hole_dia / 2)
    .extrude(bolt_head_dia)
)
valve = (
    valve
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(bolt_hole_dia / 2)
    .cutBlind(-valve_cut_depth)
)
valve = (
    valve
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(bolt_hole_dia / 2)
    .extrude(-valve_cut_depth)
)
result = valve

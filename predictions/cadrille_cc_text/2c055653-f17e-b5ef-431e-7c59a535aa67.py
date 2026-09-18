import cadquery as cq
import math
gear_thickness = 10.0
vent_diameter = 5.0
chamfer_size = 0.8
vent_radius = gear_thickness / 2.0
vent_radius = gear_radius + 2.0
vent_angle = 360.0 / vent_angle
gear_thickness = gear_thickness
gear_height = gear_thickness
gear_center_radius = gear_thickness / 2.0
gear_center_z = gear_center_radius + gear_height / 2.0
gear = (
    cq.Workplane('XY')
    .circle(vent_radius)
    .extrude(gear_thickness)
)
gear = gear.edges().chamfer(chamfer_size)
result = gear

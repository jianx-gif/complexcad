import cadquery as cq
import math
core_diameter = 30.0
core_length = 60.0
thread_pitch = 5.0
thread_height = 2.0
gear_outer_diameter = 50.0
gear_tooth_depth = 5.0
gear_tooth_height = 12.0
gear_tooth_angle = 12.0
num_teeth = 20
fillet_radius = 0.5
core = cq.Workplane('XY').circle(core_diameter/2).extrude(core_length)
helix = cq.Wire.makeHelix(pitch=thread_pitch, height=core_length, radius=core_diameter/2 + thread_height/2)
profile = cq.Workplane('XZ').polyline([(0,0), (thread_pitch/2, thread_height), (thread_pitch,0)]).close().translate((core_diameter/2 + thread_height/2, 0, 0))
thread = profile.sweep(helix, isFrenet=True)
worm = core.union(thread)
gear_body = cq.Workplane('XY').circle(gear_outer_diameter/2).extrude(gear_tooth_height)
half_angle = gear_tooth_angle/2
r_inner = gear_outer_diameter/2 - gear_tooth_depth
r_outer = gear_outer_diameter/2
points = [
    (r_inner*math.cos(math.radians(-half_angle)), r_inner*math.sin(math.radians(-half_angle))),
    (r_outer*math.cos(0), r_outer*math.sin(0)),
    (r_inner*math.cos(math.radians(half_angle)), r_inner*math.sin(math.radians(half_angle)))
]
tooth = cq.Workplane('XY').polyline(points).close().extrude(gear_tooth_height)
cut_volume = cq.Workplane('XY')
for i in range(num_teeth):
    cut_volume = cut_volume.union(tooth.rotate((0,0,0), (0,0,1), i*360/num_teeth))
gear = gear_body.cut(cut_volume)
gear = gear.edges('|Z').fillet(fillet_radius)
result = worm.union(gear)
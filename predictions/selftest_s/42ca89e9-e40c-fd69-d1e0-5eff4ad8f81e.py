import cadquery as cq
import math
module = 2.0
num_teeth = 20
gear_thickness = 20.0
hub_length = gear_thickness * 0.6
chamfer = 0.5
keyway_width = 3.0
keyway_depth = 2.0
keyway_length = hub_length * 0.5
pitch_dia = module * num_teeth
pitch_radius = pitch_dia / 2.0
addendum = module
dedendum = 1.25 * module
outer_radius = pitch_radius + addendum
root_radius = pitch_radius - dedendum
small_hub_dia = pitch_dia * 0.5
small_hub_radius = small_hub_dia / 2.0
gear_cyl = cq.Workplane('XY').circle(outer_radius).extrude(gear_thickness)
circular_pitch = math.pi * module
tooth_gap_width = circular_pitch / 2.0
pts = [
    (root_radius, -tooth_gap_width/2),
    (outer_radius, -tooth_gap_width/2),
    (outer_radius, tooth_gap_width/2),
    (root_radius, tooth_gap_width/2)
]
gap = (cq.Workplane('XY')
       .polyline(pts)
       .close()
       .extrude(gear_thickness))
gear = gear_cyl
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    gear = gear.cut(gap.rotate((0,0,0), (0,0,1), angle))
hub = cq.Workplane('XY').add(cq.Solid.makeCone(small_hub_radius, root_radius, hub_length))
gear_with_hub = gear.union(hub)
keyway = (cq.Workplane('XY')
           .box(keyway_width, keyway_length, keyway_depth)
           .translate((small_hub_radius - keyway_width/2, 0, keyway_depth/2)))
result = gear_with_hub.cut(keyway).edges("|Z").chamfer(chamfer)

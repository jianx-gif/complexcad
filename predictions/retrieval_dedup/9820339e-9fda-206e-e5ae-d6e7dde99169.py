import cadquery as cq

hub_diameter = 40.0
hub_length = 20.0
central_hole_diameter = 10.0
tooth_height = 8.0
tooth_width = 6.0
number_of_teeth = 5
twist_angle = 360 * number_of_teeth
chamfer_distance = 0.5
side_hole_diameter = 4.0
side_hole_offset = hub_diameter/2 - 5.0

hub = cq.Workplane('XY').circle(hub_diameter/2).extrude(hub_length)
hub = hub.edges('>Z').chamfer(chamfer_distance)

tooth_profile = (
    cq.Workplane('XY')
    .center(hub_diameter/2, 0)
    .rect(tooth_height, tooth_width)
)

tooth_solid = tooth_profile.twistExtrude(hub_length, twist_angle)

gear = hub.cut(tooth_solid)

gear = gear.faces('>Z').workplane().hole(central_hole_diameter)

gear = (
    gear.workplane(offset=hub_length/2)
    .pushPoints([
        (side_hole_offset, 0),
        (-side_hole_offset/2, side_hole_offset*0.8660254),
        (-side_hole_offset/2, -side_hole_offset*0.8660254)
    ])
    .hole(side_hole_diameter)
)

result = gear
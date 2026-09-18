import cadquery as cq
hub_length = 30.0
shoulder_length = 20.0
shoulder_radius = 8.0
shoulder_radius = 12.0
hub_radius = 20.0
hub_length = 10.0
tab_length = 15.0
tab_width = 8.0
tab_height = 6.0
slot_width = 6.0
slot_depth = 5.0
slot_count = 4
tab_fillet_radius = 1.0
tab_hole_diameter = 3.0
profile = (
    cq.Workplane("XZ")
    .moveTo(hub_radius, 0)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius + shoulder_length, hub_length)
    .lineTo(hub_radius + shoulder_length, hub_length + shoulder_length)
    .lineTo(hub_radius + shoulder_length, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length + shoulder_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .lineTo(hub_radius, hub_length)
    .close()
    .cutBlind(-hub_length)
)
result = (
    cq.Workplane("XY")
    .center(hub_radius + shoulder_length/2, 0)
    .circle(tab_hole_d
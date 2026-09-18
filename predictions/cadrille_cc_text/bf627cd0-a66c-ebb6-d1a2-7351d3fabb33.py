import cadquery as cq
hub_base_radius = 15.0
hub_top_radius = 25.0
hub_length = 30.0
flange_outer_radius = 45.0
flange_thickness = 5.0
key_slot_width = 6.0
key_slot_depth = 4.0
key_slot_height = hub_length - key_slot_depth
key_slot_center_radius = hub_top_radius + key_slot_depth/2
chamfer_distance = 1.0
fillet_radius = 2.0
profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (hub_base_radius, 0),
        (hub_base_radius, hub_length - flange_thickness),
        (hub_base_radius, hub_length - flange_thickness),
        (hub_base_radius, hub_length),
        (0, hub_length),
    ])
    .close()
)
hub = profile.revolve()
key_slot = (
    cq.Workplane("XY")
    .center(hub_top_radius + key_slot_depth/2, hub_length - key_slot_height/2)
    .rect(key_slot_width, key_slot_depth)
    .extrude(key_slot_height)
)
hub = hub.cut(key_slot)
key_slot = (
    cq.Workplane("XY")
    .center(0, hub_length - key_slot_height/2)
    .rect(key_slot_width, key_slot_depth)
    .extrude(key_slot_height)
)
hub = hub.cut(key_slot)
result = hub

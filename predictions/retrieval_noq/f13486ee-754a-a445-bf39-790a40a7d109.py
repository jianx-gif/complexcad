import cadquery as cq

cap_diameter = 80.0
cap_height = 45.0
wall_thickness = 2.0
rib_height = 8.0
rib_width = 6.0
top_fillet_radius = 5.0
base_radius = cap_diameter / 2.0
rib_base_z = cap_height * 0.6
rib_top_z = rib_base_z + rib_height

profile = (
    cq.Workplane('XZ')
    .moveTo(0,0)
    .lineTo(base_radius,0)
    .lineTo(base_radius, rib_base_z)
    .lineTo(base_radius+rib_width, rib_base_z)
    .lineTo(base_radius+rib_width, rib_top_z)
    .lineTo(base_radius, rib_top_z)
    .lineTo(base_radius, cap_height - top_fillet_radius)
    .threePointArc((base_radius - top_fillet_radius, cap_height - top_fillet_radius), (0, cap_height))
    .close()
)
solid = profile.revolve(360, (0,0,1))
hollow = solid.shell(-wall_thickness)
result = hollow

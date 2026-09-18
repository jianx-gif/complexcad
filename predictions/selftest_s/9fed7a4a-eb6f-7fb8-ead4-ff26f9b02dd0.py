import cadquery as cq

outer_radius = 45.0
inner_radius = 30.0
block_height = 70.0
fillet_radius = 5.0
rib_thickness = 4.0
rib_height = 55.0
rib_margin = 5.0
num_profile_ribs = 3
blind_hole_diameter = 12.0
blind_hole_depth = 25.0
chamfer_size = 1.5

rib_spacing = (block_height - 2 * rib_margin - rib_height) / (num_profile_ribs - 1)

profile = cq.Workplane('XZ').moveTo(inner_radius, 0)
base_z = 0
rib_base = rib_margin
for i in range(num_profile_ribs):
    profile = profile.lineTo(inner_radius, rib_base)
    profile = profile.lineTo(inner_radius + rib_thickness, rib_base)
    profile = profile.lineTo(inner_radius + rib_thickness, rib_base + rib_height)
    profile = profile.lineTo(inner_radius, rib_base + rib_height)
    rib_base += rib_spacing
profile = profile.lineTo(inner_radius, block_height)
profile = profile.lineTo(outer_radius, block_height)
profile = profile.lineTo(outer_radius, 0)
profile = profile.threePointArc((outer_radius - fillet_radius, -fillet_radius), (inner_radius, 0))
profile = profile.close()
result = profile.revolve()
result = (
    result.faces('>Z')
    .workplane()
    .hole(blind_hole_diameter, blind_hole_depth)
)
result = result.edges('>Z').chamfer(chamfer_size)

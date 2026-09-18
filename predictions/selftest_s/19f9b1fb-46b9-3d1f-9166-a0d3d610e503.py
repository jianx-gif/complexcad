import cadquery as cq

outer_diameter = 80.0
inner_diameter = 40.0
ring_width = (outer_diameter - inner_diameter) / 2
base_thickness = 12.0
boss_radius = 8.0
boss_height = 6.0
rib_width = 5.0
rib_height = 8.0
blind_hole_diameter = 6.0
blind_hole_depth = 8.0
num_holes = 5
chamfer_size = 1.0

inner_radius = inner_diameter / 2.0
outer_radius = outer_diameter / 2.0

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, base_thickness)
    .lineTo(inner_radius + boss_radius, base_thickness)
    .lineTo(inner_radius + boss_radius, base_thickness + boss_height)
    .lineTo(inner_radius, base_thickness + boss_height)
    .lineTo(inner_radius, base_thickness)
    .lineTo(outer_radius - rib_width, base_thickness)
    .lineTo(outer_radius - rib_width, base_thickness + rib_height)
    .lineTo(outer_radius, base_thickness + rib_height)
    .lineTo(outer_radius, base_thickness)
    .close()
)

solid = profile.revolve()

hole_radius_position = inner_radius + boss_radius + (ring_width - boss_radius) / 2.0

result = (
    solid
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius_position, startAngle=0, angle=360, count=num_holes)
    .hole(blind_hole_diameter, depth=blind_hole_depth)
    .edges("|Z")
    .chamfer(chamfer_size)
)

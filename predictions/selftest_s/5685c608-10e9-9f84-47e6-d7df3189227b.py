import cadquery as cq

base_radius = 20.0
bellows_length = 60.0
corrugation_count = 6
corrugation_height = 4.0
flange_thickness = 6.0
flange_outer_radius = 35.0
inner_flange_outer_radius = 30.0
flange_chamfer = 1.0
hole_diameter = 4.0
hole_count = 6
hole_offset = 2.0
boss_radius = base_radius / 2.0
boss_height = 5.0

pitch = bellows_length / corrugation_count
points = [(0, 0), (base_radius, 0)]
for i in range(corrugation_count):
    z_start = i * pitch
    z_mid = z_start + pitch / 2.0
    z_end = (i + 1) * pitch
    points.append((base_radius + corrugation_height, z_mid))
    points.append((base_radius, z_end))
points.append((0, bellows_length))

bellows = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()
)

outer_flange = (
    cq.Workplane("XY", origin=(0, 0, bellows_length))
    .circle(flange_outer_radius)
    .extrude(flange_thickness)
)

inner_flange = (
    cq.Workplane("XY", origin=(0, 0, bellows_length))
    .circle(inner_flange_outer_radius)
    .extrude(flange_thickness)
)

flanges = outer_flange.union(inner_flange).edges().chamfer(flange_chamfer)

boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
)

hole_radius = flange_outer_radius - hole_offset
hole_cylinders = (
    cq.Workplane("XY", origin=(0, 0, bellows_length + flange_thickness))
    .polarArray(count=hole_count, startAngle=0, angle=360, radius=hole_radius)
    .circle(hole_diameter / 2.0)
    .extrude(-flange_thickness * 2)
)

result = bellows.union(flanges).union(boss).cut(hole_cylinders)

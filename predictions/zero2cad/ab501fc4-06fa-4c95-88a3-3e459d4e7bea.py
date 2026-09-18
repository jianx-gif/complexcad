import cadquery as cq

# Parameters
outer_radius = 45.0
inner_radius = 35.0
flange_thickness = 8.0
boss_radius = 12.0
boss_height = 12.0
hole_diameter = 8.0
countersink_diameter = 12.0
countersink_depth = 4.0
hole_circle_radius = 30.0
num_holes = 8
chamfer_size = 1.0
rib_width = 4.0
rib_height = 6.0
rib_spacing = 20.0
rib_count = 3
rib_offset = 5.0

# Base flange via revolve of a rectangular profile
flange = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, flange_thickness)
    .lineTo(inner_radius, flange_thickness)
    .close()
    .revolve()
)

# Central boss on top of flange
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, flange_thickness))
)

# Combine flange and boss
part = flange.union(boss)

# Add radial ribs on the inner side of the flange (bottom face)
for i in range(rib_count):
    angle = i * 360.0 / rib_count
    rib = (
        cq.Workplane("XY")
        .center(inner_radius - rib_offset, 0)
        .rect(rib_width, rib_height)
        .extrude(flange_thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    part = part.union(rib)

# Countersunk holes pattern on top face
part = (
    part.faces(">Z")
    .workplane()
    .polarArray(radius=hole_circle_radius, startAngle=0, angle=360, count=num_holes)
    .cskHole(hole_diameter, countersink_diameter, countersink_depth)
)

# Chamfer outer vertical edges
part = part.edges("|Z").chamfer(chamfer_size)

result = part
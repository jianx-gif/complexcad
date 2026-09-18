import cadquery as cq

# Parameters
outer_length = 90.0
outer_width = 60.0
outer_height = 30.0
wall_thickness = 2.0
boss_diameter = 20.0
boss_height = 10.0
chamfer_distance = 3.0
mount_hole_diameter = 2.0
mount_hole_spacing_x = 60.0
mount_hole_spacing_y = 40.0
mount_hole_offset_x = (outer_length - mount_hole_spacing_x) / 2.0
mount_hole_offset_y = (outer_width - mount_hole_spacing_y) / 2.0
rib_thickness = 2.0
rib_height = 5.0
rib_spacing = 15.0

# Base solid
base = (
    cq.Workplane("XY")
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
)

# Internal cavity (leaving bottom wall)
inner_cavity = (
    cq.Workplane("XY")
    .box(
        outer_length - 2 * wall_thickness,
        outer_width - 2 * wall_thickness,
        outer_height - wall_thickness,
        centered=(True, True, False),
    )
    .translate((0, 0, wall_thickness))
)

# Subtract cavity to create walls
housing = base.cut(inner_cavity)

# Central boss on interior bottom
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
    .translate((0, 0, wall_thickness))
)

housing = housing.union(boss)

# Chamfer rear face (negative Z)
housing = housing.faces("<Z").edges().chamfer(chamfer_distance)

# Mounting holes on top face
hole_positions = [
    (-mount_hole_offset_x, -mount_hole_offset_y),
    (mount_hole_offset_x, -mount_hole_offset_y),
    (-mount_hole_offset_x, mount_hole_offset_y),
    (mount_hole_offset_x, mount_hole_offset_y),
]

housing = (
    housing.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

# Internal ribs for stiffness (grid pattern)
rib = (
    cq.Workplane("XY")
    .box(rib_thickness, outer_width - 2 * wall_thickness, rib_height, centered=(True, True, False))
    .translate((0, 0, wall_thickness + rib_height / 2.0))
)

rib_count = int((outer_length - 2 * wall_thickness) // rib_spacing)
for i in range(rib_count):
    x_offset = - (outer_length / 2.0 - wall_thickness) + rib_spacing / 2.0 + i * rib_spacing
    housing = housing.union(rib.translate((x_offset, 0, 0)))

result = housing
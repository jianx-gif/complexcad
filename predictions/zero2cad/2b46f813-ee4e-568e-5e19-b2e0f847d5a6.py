import cadquery as cq

# Parameters
outer_diameter = 80.0
wall_thickness = 5.0
length = 50.0
flange_diameter = 100.0
flange_thickness = 10.0
fillet_radius = 5.0
rib_width = 4.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = int((length - 2 * fillet_radius) // rib_spacing)
boss_diameter = 20.0
boss_height = 8.0
boss_offset = 10.0
slot_width = 6.0
slot_length = 30.0
slot_depth = 3.0

# Base cylinder
base = cq.Workplane("XY").circle(outer_diameter / 2).extrude(length)
# Flange on top
flange = (
    cq.Workplane("XY", origin=(0, 0, length))
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)
# Combine base and flange
housing = base.union(flange)
# Shell to create wall thickness
housing = housing.shell(-wall_thickness)
# Fillet on outer edge of flange
housing = housing.faces(">Z").edges().fillet(fillet_radius)
# Internal ribs
rib = (
    cq.Workplane("XZ")
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
for i in range(rib_count):
    z_pos = fillet_radius + i * rib_spacing
    rib_instance = rib.translate((0, 0, z_pos))
    housing = housing.union(rib_instance)
# Mounting boss on side
boss = (
    cq.Workplane("XY")
    .center(-outer_diameter / 2 + boss_offset, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)
housing = housing.union(boss)
# Slot on side wall
slot = (
    cq.Workplane("XZ")
    .center(0, length / 2)
    .rect(slot_width, slot_length)
    .extrude(slot_depth)
    .translate((outer_diameter / 2 - wall_thickness / 2, 0, 0))
)
housing = housing.cut(slot)
result = housing
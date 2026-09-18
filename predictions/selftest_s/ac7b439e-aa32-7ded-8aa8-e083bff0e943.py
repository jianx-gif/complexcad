import cadquery as cq

arm_length = 80
arm_width = 30
arm_thickness = 20
tip_length = 15
tip_radius = 10
shell_thickness = 2
cell_diameter = 6
fillet_radius = 3
rib_width = 20
rib_thickness = 3
slot_width = 5
slot_height = 10

# Base rectangular beam with fillet
beam = (cq.Workplane('XY')
        .box(arm_width, arm_thickness, arm_length - tip_length)
        .translate((0, 0, (arm_length - tip_length) / 2)))
beam = beam.edges().fillet(fillet_radius)

# Tip cylinder with fillet
tip = (cq.Workplane('XY')
        .cylinder(tip_length, tip_radius * 2)
        .translate((0, 0, arm_length - tip_length / 2)))
tip = tip.edges().fillet(fillet_radius)

# Combine beam and tip
outer = beam.union(tip)

# Add a rectangular rib inside for stiffness
rib = (cq.Workplane('XY')
       .rect(rib_width, rib_thickness)
       .extrude(arm_length - tip_length - 2 * shell_thickness)
       .translate((0, 0, (arm_length - tip_length) / 2)))
outer = outer.union(rib)

# Add a side slot for cable routing
slot = (cq.Workplane('XY')
        .rect(slot_width, slot_height)
        .extrude(arm_thickness + 2)
        .translate((arm_width / 2 + slot_width / 2, 0, arm_length / 2)))
outer = outer.cut(slot)

# Interior honeycomb core dimensions
interior_width = arm_width - 2 * shell_thickness
interior_thickness = arm_thickness - 2 * shell_thickness
interior_length = arm_length - tip_length - 2 * shell_thickness

inner_block = (cq.Workplane('XY')
               .box(interior_width, interior_thickness, interior_length)
               .translate((0, 0, (arm_length - tip_length) / 2)))

hex_prism = (cq.Workplane('XY')
            .polygon(6, cell_diameter)
            .extrude(interior_length))

count_x = max(int(interior_width / (cell_diameter * 1.2)), 1)
count_y = max(int(interior_thickness / (cell_diameter * 1.2)), 1)

x_spacing = interior_width / count_x
y_spacing = interior_thickness / count_y

positions = []
for i in range(count_x):
    for j in range(count_y):
        x = -interior_width / 2 + x_spacing / 2 + i * x_spacing
        y = -interior_thickness / 2 + y_spacing / 2 + j * y_spacing
        positions.append((x, y))

hex_array = (cq.Workplane('XY')
            .pushPoints(positions)
            .polygon(6, cell_diameter)
            .extrude(interior_length))

honeycomb = inner_block.cut(hex_array)

result = outer.union(honeycomb)

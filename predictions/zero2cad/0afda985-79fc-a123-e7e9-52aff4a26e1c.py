import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 12.0
arm_thickness = 8.0
boss_diameter = 20.0
boss_height = 30.0
hole_diameter = 6.0
hole_spacing = 20.0
hole_count = 3
chamfer_size = 1.0
rib_height = 4.0
rib_thickness = 3.0
rib_spacing = 15.0

# Base arm extruded along Z
arm = (
    cq.Workplane("XY")
    .rect(arm_width, arm_thickness)
    .extrude(arm_length, both=True)
)

# Central cylindrical boss at mid-length
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    .translate((0, 0, -boss_height / 2))
)

# Combine arm and boss
result = arm.union(boss)

# Add ribs on the +Y side of the arm
rib_count = int((arm_length - rib_spacing) // rib_spacing) + 1
for i in range(rib_count):
    z_pos = -arm_length / 2 + rib_spacing / 2 + i * rib_spacing
    rib = (
        cq.Workplane("XY")
        .center(0, arm_thickness / 2 + rib_thickness / 2)
        .rect(rib_thickness, rib_height)
        .extrude(arm_width)
        .translate((0, 0, z_pos))
    )
    result = result.union(rib)

# Apply chamfer to all outer edges
result = result.edges().chamfer(chamfer_size)

# Drill three through holes on the +Y side, spaced along Z
for i in range(hole_count):
    z_pos = -arm_length / 2 + hole_spacing / 2 + i * hole_spacing
    result = (
        result.faces(">Y")
        .workplane()
        .center(0, z_pos)
        .hole(hole_diameter)
    )

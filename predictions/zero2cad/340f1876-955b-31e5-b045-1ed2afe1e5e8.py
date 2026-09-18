import cadquery as cq

# Dimensions
base_length = 80.0
base_width = 80.0
base_thickness = 5.0
frame_outer_radius = 35.0
frame_inner_radius = 25.0
frame_height = 10.0
boss_radius = 10.0
boss_height = 8.0
hole_diameter = 5.0
hole_pattern_radius = 30.0
chamfer_size = 0.5
rib_thickness = 3.0
rib_height = 12.0
rib_offset = 10.0

# Base plate
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness, centered=(True, True, False))
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Raised circular frame (ring) on top of base
frame = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(frame_outer_radius)
    .extrude(frame_height)
    .faces(">Z")
    .workplane()
    .circle(frame_inner_radius)
    .cutBlind(-frame_height)
    .edges(">Z")
    .chamfer(chamfer_size/2)
)

# Central boss
boss = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(boss_radius)
    .extrude(boss_height)
)

# Reinforcement ribs on the base (two orthogonal ribs)
rib1 = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(rib_thickness, base_length - 2 * rib_offset)
    .extrude(rib_height)
)

rib2 = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(base_width - 2 * rib_offset, rib_thickness)
    .extrude(rib_height)
)

# Assemble main body
assembled = base.union(frame).union(boss).union(rib1).union(rib2)

# Add five through holes in a circular pattern on the top surface
result = (
    assembled
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_pattern_radius, count=5, startAngle=0, angle=360)
    .hole(hole_diameter)
)

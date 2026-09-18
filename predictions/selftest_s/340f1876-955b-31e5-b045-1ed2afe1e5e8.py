import cadquery as cq

# Dimensions
base_length = 80.0
base_width = 80.0
base_thickness = 5.0
base_chamfer = 0.5
frame_outer_diameter = 70.0
frame_inner_diameter = 50.0
frame_height = 10.0
rib_thickness = 3.0
central_boss_diameter = 20.0
central_boss_height = 8.0
star_radius = 30.0
star_hole_count = 5
hole_diameter = 5.0
chamfer_edge = 0.3

# Base plate
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness, centered=(True, True, False))
    .edges("|Z").chamfer(base_chamfer)
)

# Ribs and circular frame (raised ring) positioned on top of base
frame_and_ribs = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(rib_thickness, frame_outer_diameter)
    .extrude(frame_height, combine=True)
    .workplane(offset=base_thickness)
    .rect(frame_outer_diameter, rib_thickness)
    .extrude(frame_height, combine=True)
    .workplane(offset=base_thickness)
    .circle(frame_outer_diameter / 2.0)
    .circle(frame_inner_diameter / 2.0)
    .extrude(frame_height, combine=True)
)

# Central boss on top of frame
boss = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness + frame_height)
    .circle(central_boss_diameter / 2.0)
    .extrude(central_boss_height)
)

# Assemble all components and add features
result = (
    base.union(frame_and_ribs).union(boss)
    .faces(">Z").edges().chamfer(chamfer_edge)
    .faces(">Z").workplane()
    .polarArray(star_radius, 0, 360, star_hole_count)
    .hole(hole_diameter)
)

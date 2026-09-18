import cadquery as cq
import math

base_width = 80.0
base_length = 60.0
base_thickness = 5.0
frame_width = 5.0
frame_height = 8.0
boss_radius = 8.0
boss_height = 3.0
hole_diameter = 4.0
hole_offset_from_edge = 10.0
chamfer_size = 0.5
hole_center_radius = min(base_width, base_length) / 2 - frame_width - hole_offset_from_edge
hole_positions = [(hole_center_radius * math.cos(math.radians(i * 60)),
                  hole_center_radius * math.sin(math.radians(i * 60))) for i in range(6)]

# Base plate
base_plate = (
    cq.Workplane("XY")
    .box(base_width, base_length, base_thickness, centered=(True, True, False))
)

# Raised frame outer block
frame_outer = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, base_thickness))
    .rect(base_width, base_length)
    .extrude(frame_height, combine=False)
)
# Inner cut to create hollow in frame
frame_inner_cut = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, base_thickness))
    .rect(base_width - 2 * frame_width, base_length - 2 * frame_width)
    .extrude(frame_height, combine=False)
)
frame_shell = frame_outer.cut(frame_inner_cut)
# Central boss
boss = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, base_thickness))
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_height, combine=False)
)
frame_with_boss = frame_shell.union(boss)

# Combine base and frame
combined = base_plate.union(frame_with_boss)
# Chamfer outer vertical edges of the raised frame
combined = combined.edges("|Z").chamfer(chamfer_size)
# Drill peripheral screw holes
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

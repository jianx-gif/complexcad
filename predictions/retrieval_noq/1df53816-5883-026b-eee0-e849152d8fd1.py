import cadquery as cq
import math
from types import SimpleNamespace as Measures

params = Measures(
    side_length = 80.0,
    thickness = 10.0,
    fillet_radius = 2.0,
    clearance_hole_diameter = 8.0,
    clearance_hole_offset = 20.0,
    arc_block_radius = 15.0,
    arc_block_depth = 5.0,
    arc_block_width = 4.0,
    arc_block_angle = 60.0,
    arc_block_sweep_thickness = 3.0
)

params.triangle_height = (math.sqrt(3) / 2) * params.side_length
centroid_y = -params.triangle_height / 3
params.centroid = (0.0, centroid_y)

tri = (
    cq.Workplane("XY")
    .moveTo(-params.side_length/2, centroid_y)
    .lineTo(params.side_length/2, centroid_y)
    .lineTo(0, centroid_y + params.triangle_height)
    .close()
)

plate = tri.extrude(params.thickness)

plate = (
    plate.faces("<Z").workplane()
    .center(0, centroid_y + params.triangle_height/2)
    .rect(params.side_length*0.2, params.thickness*0.5)
    .cutBlind(params.thickness*0.2)
)

plate = plate.edges("|Z").fillet(params.fillet_radius)

hole_x = params.centroid[0] + params.clearance_hole_offset
hole_y = params.centroid[1]
plate = (
    plate.faces(">Z").workplane()
    .center(hole_x, hole_y)
    .hole(params.clearance_hole_diameter)
)

arc_path = (
    cq.Workplane("XY")
    .radiusArc(
        (params.arc_block_radius * math.cos(math.radians(params.arc_block_angle/2)),
         params.arc_block_radius * math.sin(math.radians(params.arc_block_angle/2))),
        params.arc_block_radius)
    .wire()
)

arc_block = (
    cq.Workplane("XY")
    .transformed(
        rotate=(90, -params.arc_block_angle/2, 0),
        offset=(0, 0, params.thickness/2)
    )
    .rect(params.arc_block_depth, params.arc_block_width)
    .sweep(arc_path, transition="round")
)

result = plate.union(arc_block)

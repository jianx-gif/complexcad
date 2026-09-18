import cadquery as cq
import math

block_length = 60.0
block_width = 40.0
block_height = 20.0
draft_angle = 3.0
hole_diameter = 10.0
hole_offset_x = 15.0
hole_offset_y = 0.0
rib_thickness = 4.0
rib_height = 5.0
rib_spacing = 20.0
rib_margin = 5.0
fillet_radius = 1.0
tab_length = 30.0
tab_width = 8.0

base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height, taper=draft_angle)
)

tab = (
    cq.Workplane("XY")
    .center(block_length/2 + tab_length/2, 0)
    .rect(tab_length, tab_width)
    .extrude(block_height, taper=draft_angle)
)

result = base.union(tab)

result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_offset_x, hole_offset_y)
    .hole(hole_diameter)
)

rib_count = int((block_length - 2 * rib_margin) // rib_spacing) + 1
rib_positions = [(-block_length/2 + rib_margin + i * rib_spacing) for i in range(rib_count)]

ribs = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(x, 0) for x in rib_positions])
    .rect(rib_thickness, block_width - 2 * rib_margin)
    .extrude(rib_height)
)

result = result.union(ribs)

result = result.edges("|Z").fillet(fillet_radius)

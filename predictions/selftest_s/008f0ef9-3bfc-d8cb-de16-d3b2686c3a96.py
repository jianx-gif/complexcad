import cadquery as cq
import math

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
rib_height = 3.0
rib_offset = 5.0
hole_diameter = 8.0
countersink_diameter = 12.0
countersink_angle = 82.0
hole_spacing_x = 20.0
hole_spacing_y = 20.0
hole_margin_x = 15.0
hole_margin_y = 15.0
chamfer_size = 0.8

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

top_wp = base.faces(">Z").workplane()
outer_rib = top_wp.rect(plate_length, plate_width).extrude(rib_height)
inner_cut = top_wp.rect(plate_length - 2 * rib_offset, plate_width - 2 * rib_offset).extrude(rib_height + 0.01)
rib = outer_rib.cut(inner_cut)
plate_with_rib = base.union(rib)

num_x = int((plate_length - 2 * hole_margin_x) // hole_spacing_x) + 1
num_y = int((plate_width - 2 * hole_margin_y) // hole_spacing_y) + 1
x_vals = [hole_margin_x + i * hole_spacing_x for i in range(num_x)]
y_vals = [hole_margin_y + i * hole_spacing_y for i in range(num_y)]
points = [(x - plate_length / 2, y - plate_width / 2) for x in x_vals for y in y_vals]

result = (
    plate_with_rib
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, depth=plate_thickness + rib_height)
    .edges("|Z")
    .chamfer(chamfer_size)
)

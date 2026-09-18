import cadquery as cq
import math
plate_width = 80.0
plate_height = 60.0
plate_thickness = 8.0
boss_radius = 10.0
recess_radius = 15.0
recess_depth = 2.0
hole_diameter = 6.0
countersink_diameter = 10.0
countersink_angle = 90.0
countersink_depth = 3.0
hole_spacing_x = 25.0
hole_spacing_y = 20.0
hole_cols = 3
hole_rows = 2
chamfer_distance = 1.0
offset_x = (hole_cols - 1) * hole_spacing_x / 2
offset_y = (hole_rows - 1) * hole_spacing_y / 2
grid_points = [(i * hole_spacing_x - offset_x, j * hole_spacing_y - offset_y) for i in range(hole_cols) for j in range(hole_rows)]
base = (cq.Workplane("XY")
        .rect(plate_width, plate_height)
        .center(plate_width/2 - boss_radius - 5, 0)
        .circle(boss_radius)
        .extrude(plate_thickness))
recess = (cq.Workplane("XY")
          .center(0, 0)
          .circle(recess_radius)
          .extrude(-recess_depth))
result = (base.cut(recess)
          .faces(">Z")
          .workplane()
          .pushPoints(grid_points)
          .cskHole(hole_diameter, countersink_diameter, countersink_angle, plate_thickness + countersink_depth)
          .edges("|Z")
          .chamfer(chamfer_distance))

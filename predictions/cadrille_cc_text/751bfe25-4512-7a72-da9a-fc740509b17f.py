import cadquery as cq
import math
disc_diameter = 80.0
disc_thickness = 5.0
rim_radial_thickness = 5.0
rim_height = 4.0
chamfer = 0.5
boss_diameter = 20.0
boss_height = 3.0
countersink_diameter = 8.5
countersink_depth = 2.0
radius_offset = 0.0
outer_radius = disc_diameter / 2.0
inner_radius = radius_radius - rim_radial_thickness
outer_cyl = cq.Workplane('XZ').circle(outer_radius).extrude(disc_thickness)
rim = cq.Workplane('XY').cylinder(rim_radial_thickness, inner_radius)
rim = rim.edges().chamfer(chamfer)
result = rim

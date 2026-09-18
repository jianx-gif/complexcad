import cadquery as cq
import math
elbow_radius = 5.0
chute_max_radius = 30.0
chute_height = 80.0
wall_thickness = 3.0
inlet_bevel_radius = 5.0
inlet_bevel_radius = chute_max_radius - wall_thickness
chamfer_size = 1.0
outer_radius = (inlet_bevel_radius) / 2.0
inner_radius = inner_radius - wall_thickness
outer_cyl = cq.Workplane('XZ').cylinder(chute_height, outer_radius)
outer_cyl = cq.Workplane('XY').cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = cq.Workplane('XY').cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
outer_cyl = outer_cyl.workplane(offset=0).cylinder(chute_height, outer_radius - wall_thickness)
result = outer_cyl.union(outer_cyl)

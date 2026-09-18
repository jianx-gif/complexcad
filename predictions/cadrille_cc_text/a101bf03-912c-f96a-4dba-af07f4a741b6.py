import cadquery as cq
import math
inlet_radius = 18.0
wall_thickness = 3.0
flange_outer_radius = 8.0
flange_thickness = 5.0
flange_outer_radius = 30.0
wall_thickness = 4.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
boss_thickness = 4.0
boss_height = 6.0
boss_width = 8.0
boss_offset = inlet_radius - wall_thickness/2
chamfer_size = 0.8
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(inlet_radius, 0)
    .lineTo(inlet_radius, flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness)
    .lineTo(flange_outer_radius, inlet_radius)
    .lineTo(inlet_radius, inlet_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
boss = (
    cq.Workplane("XY")
    .box(boss_width, boss_thickness, boss_height)
    .translate((0, 0, wall_thickness))
)
solid = solid.cut(boss)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
mount_holes = (
    cq.Workplane("XY")
    .center(inlet_radius + wall_thickness/2, 0)
    .box(inlet_radius, boss_width, boss_height)
)
solid = solid.cut(mount_holes)
boss = (
    cq.Workplane("XY")
    .center(inlet_radius + wall_thickness/2, 0)
    .circle(boss_width/2)
    .extrude(boss_height)
)
solid = solid.union(boss)
result = solid

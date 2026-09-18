import cadquery as cq
import math
outer_diameter = 30.0
wall_thickness = 4.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 6
hole_offset = 15.0
chamfer_distance = 0.5
outer_radius = outer_diameter / 2
inner_radius = inner_radius + wall_thickness
base = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius + wall_thickness, wall_thickness + outer_radius)
    .lineTo(inner_radius + wall_thickness, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = base.cut(inner_radius)
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter)
result = solid

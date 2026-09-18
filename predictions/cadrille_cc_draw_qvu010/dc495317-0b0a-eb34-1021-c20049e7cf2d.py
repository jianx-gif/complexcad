import cadquery as cq
import math
outer_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
rib_width = 4.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 10.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_offset = wall_thickness + rib_height / 2.0
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius + rib_width, wall_thickness)
    .lineTo(inner_radius + rib_width, wall_thickness + rib_height)
    .lineTo(inner_radius + rib_width, wall_thickness + rib_height)
    .lineTo(inner_radius, wall_thickness + rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_width / 2.0, wall_thickness + rib_height / 2.0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
]
solid = (
    solid.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid

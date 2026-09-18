import cadquery as cq
import math

# Parameters
outer_radius = 30.0
wall_thickness = 1.5
inner_radius = outer_radius - wall_thickness
tube_length = 80.0
hole_diameter = 4.0
hole_count = 8
hole_spacing = tube_length / 4.0
chamfer_size = 0.4
rib_width = 3.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 20.0

# Base thin-walled tube
tube = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, tube_length)
    .lineTo(inner_radius, tube_length)
    .close()
    .revolve()
)

# Chamfer top and bottom rim edges
tube = tube.faces(">Z").edges().chamfer(chamfer_size)
tube = tube.faces("<Z").edges().chamfer(chamfer_size)

# Add external ribs for stiffness (intersecting the tube)
rib_count = int(tube_length // rib_spacing)
for i in range(rib_count):
    z_pos = (i + 0.5) * rib_spacing
    rib = (
        cq.Workplane("XZ")
        .center(outer_radius - rib_thickness/2, z_pos)
        .rect(rib_thickness, rib_height)
        .extrude(rib_width)
    )
    tube = tube.union(rib)

# Create radial screw holes
hole_cuts = cq.Workplane("XY")
for i in range(hole_count):
    angle = i * 360.0 / hole_count
    for j in range(1, 4):
        z_pos = j * hole_spacing
        hole = (
            cq.Workplane("XY")
            .center(outer_radius - wall_thickness/2, 0)
            .circle(hole_diameter/2)
            .extrude(wall_thickness*2)
            .rotate((0, 0, 0), (0, 0, 1), angle)
            .translate((0, 0, z_pos))
        )
        hole_cuts = hole_cuts.union(hole)

result = tube.cut(hole_cuts)

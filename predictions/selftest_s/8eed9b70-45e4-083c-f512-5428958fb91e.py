import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 70.0
height = 30.0
wall_thickness = 2.0
lip_height = 5.0
snap_beam_width = 8.0
snap_beam_thickness = 1.0
snap_beam_length = 12.0
snap_protrusion_height = 3.0
snap_protrusion_width = 6.0
chamfer_distance = 0.8
hole_diameter = 4.0
vent_width = 4.0
vent_height = 10.0
vent_spacing = 12.0

outer_radius = outer_diameter/2.0
inner_radius = inner_diameter/2.0

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height - lip_height)
    .threePointArc((outer_radius + 2, height - lip_height/2), (outer_radius, height))
    .lineTo(0, height)
    .close()
)

solid = profile.revolve()
result = solid.shell(-wall_thickness)
result = result.edges(">>Z").chamfer(chamfer_distance)

beam = (
    cq.Workplane("XY")
    .center(outer_radius - wall_thickness - snap_beam_thickness/2, 0)
    .rect(snap_beam_width, snap_beam_thickness)
    .extrude(snap_beam_length)
)
result = result.union(beam)

protrusion = (
    cq.Workplane("XY")
    .center(outer_radius + snap_protrusion_height/2, 0)
    .cylinder(snap_protrusion_width, snap_protrusion_height)
)
result = result.union(protrusion)

vent_origin_y = -((vent_spacing)*(2-1)/2)
for i in range(2):
    result = (
        result.faces(">Z")
        .workplane()
        .center(0, vent_origin_y + i*vent_spacing)
        .rect(vent_width, vent_height)
        .cutBlind(-2.0)
    )

hole_radius = outer_radius - wall_thickness/2
for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
    x = hole_radius * math.cos(angle)
    y = hole_radius * math.sin(angle)
    cutter = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(hole_diameter/2)
        .extrude(height + 2)
    )
    result = result.cut(cutter)

rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(inner_radius - wall_thickness/2)
    .extrude(2.0)
)
result = result.union(rib)

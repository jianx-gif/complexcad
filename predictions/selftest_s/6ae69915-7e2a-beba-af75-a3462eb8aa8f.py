
import cadquery as cq

outer_radius = 45
inner_radius = 30
flange_depth = 8
ring_height = 3
fillet_radius = 2
hole_diameter = 5
hole_depth = flange_depth - 1
hole_offset_radius = (inner_radius + outer_radius) / 2
ring_radial_thickness = 5
ring_mid_radius = (inner_radius + outer_radius) / 2
ring_outer_radius = ring_mid_radius + ring_radial_thickness / 2
ring_inner_radius = ring_mid_radius - ring_radial_thickness / 2
tab_width = 12
tab_thickness = 3
tab_height = 6
mount_hole_diameter = 4

base = (
    cq.Workplane('XZ')
    .polyline([
        (inner_radius, 0),
        (inner_radius, flange_depth),
        (outer_radius, flange_depth),
        (outer_radius, 0),
    ])
    .close()
    .revolve(360)
)

base_f = base.faces('>Z').edges().fillet(fillet_radius)

base_f = (
    base_f
    .faces('>Z')
    .workplane()
    .polarArray(hole_offset_radius, startAngle=0, count=2, angle=180)
    .hole(hole_diameter, depth=hole_depth)
)

ring = (
    cq.Workplane('XY')
    .circle(ring_outer_radius)
    .extrude(ring_height)
    .faces('>Z')
    .workplane()
    .circle(ring_inner_radius)
    .cutBlind(ring_height)
    .translate((0, 0, flange_depth))
)

tabs = (
    cq.Workplane('XY')
    .polarArray(outer_radius + tab_thickness / 2, startAngle=0, count=4, angle=360)
    .rect(tab_width, tab_thickness)
    .extrude(tab_height)
    .faces('>Z')
    .workplane()
    .hole(mount_hole_diameter)
)

result = base_f.union(ring).union(tabs)

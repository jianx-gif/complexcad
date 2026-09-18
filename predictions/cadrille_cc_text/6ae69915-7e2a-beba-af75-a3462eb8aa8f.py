import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
flange_depth = 8.0
flange_radius = outer_radius - inner_radius
flange_radius = outer_radius - 2 * flange_depth
ring_radial_thickness = 5.0
ring_height = 3.0
hole_diameter = 5.0
hole_clearance = 2.0
hole_margin = 10.0
tab_width = 12.0
tab_thickness = 3.0
tab_height = 6.0
tab_width = tab_width * 0.9
profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (0, ring_radial_thickness),
        (flange_radius, ring_radial_thickness),
        (flange_radius, ring_radial_thickness + ring_height),
        (0, ring_radial_thickness + ring_height),
        (0, 0)
    ])
    .close()
)
ring = profile.revolve()
ring = ring.faces(">Z").workplane().hole(hole_diameter)
ring = ring.faces(">Z").workplane().hole(hole_clearance)
ring = ring.faces(">Z").workplane().circle(ring_radial_thickness + ring_height).cutBlind(-ring_height)
ring = ring.faces(">Z").workplane().circle(ring_radial_thickness + ring_height).cutBlind(-ring_height)
result = ring

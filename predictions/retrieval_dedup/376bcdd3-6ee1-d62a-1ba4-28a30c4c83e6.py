import cadquery as cq
outer_diameter = 50.0
outer_radius = outer_diameter/2
inner_diameter = 44.0
inner_radius = inner_diameter/2
seal_thickness = 5.0
rib_radial_extension = 1.0
rib_width = 1.0
rib_center = seal_thickness/2
shell_thickness = 0.8
points = [
    (outer_radius, 0),
    (outer_radius, seal_thickness),
    (inner_radius + rib_radial_extension, seal_thickness),
    (inner_radius + rib_radial_extension, rib_center + rib_width/2),
    (inner_radius, rib_center + rib_width/2),
    (inner_radius, rib_center - rib_width/2),
    (inner_radius + rib_radial_extension, rib_center - rib_width/2),
    (inner_radius + rib_radial_extension, 0),
]
profile = cq.Workplane('XY').polyline(points).close()
solid = profile.revolve()
result = solid.shell(shell_thickness)

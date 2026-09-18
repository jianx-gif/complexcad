import cadquery as cq
plate_width=80
plate_depth=60
plate_thickness=6
corner_radius=5
result = (
    cq.Workplane('XY')
    .sketch()
    .rect(plate_width, plate_depth)
    .vertices()
    .fillet(corner_radius)
    .finalize()
    .extrude(plate_thickness)
)

import cadquery as cq
plate_length=100
plate_width=70
plate_thickness=10
result = (
    cq.Workplane('XY')
    .sketch()
    .rect(plate_length, plate_width)
    .rect(20,20, mode='s')
    .finalize()
    .extrude(plate_thickness)
)

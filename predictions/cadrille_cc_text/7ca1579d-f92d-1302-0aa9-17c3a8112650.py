import cadquery as cq
hub_radius = 20.0
hub_thickness = 5.0
flange_width = 10.0
flange_depth = hub_thickness
flange_thickness = 3.0
flange_width = 8.0
flange_height = 40.0
flange_count = 6
chamfer_distance = 0.5
fillet_radius = 0.8
base = (
    cq.Workplane("XY")
    .circle(hub_radius)
    .extrude(hub_thickness)
)
flange = (
    cq.Workplane("XY")
    .rect(flange_width, flange_depth)
    .extrude(flange_height)
    .translate((0, 0, hub_thickness))
)
flange = (
    flange
    .edges("|Z")
    .fillet(fillet_radius)
)
flange = (
    flange
    .faces(">Z")
    .workplane()
    .polarArray(radius=hub_radius - flange_count, startAngle=0, angle=360, count=flange_count)
    .rect(flange_width, flange_height)
    .extrude(flange_thickness)
)
flange = (
    flange
    .faces(">Z")
    .workplane()
    .pushPoints([(-hub_radius, 0), (hub_radius, 0)])
    .circle(flange_depth)
    .extrude(flange_thickness)
)
flange = (
    flange
    .edges("|Z")
    .chamfer(chamfer_distance)
)
result = (
    flange
    .edges("|Z")
    .fillet(fillet_radius)
)

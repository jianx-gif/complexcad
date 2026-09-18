import cadquery as cq
base_length = 80.0
base_width = 50.0
base_thickness = 8.0
wall_thickness = 1.0
fillet_radius = 3.0
hinge_radius = 6.0
hinge_center_x = -20.0
hinge_center_y = 0.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 30.0
rib_width = 8.0
rib_height = 4.0
rib_spacing = 20.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
    .shell(-wall_thickness)
)
hinge = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(hinge_center_x, hinge_center_y)
    .extrude(hinge_center_y)
    .translate((0, 0, base_thickness))
)
hinge = (
    hinge
    .faces(">Z")
    .workplane()
    .center(hinge_center_x, 0)
    .hole(hinge_diameter)
    .center(hinge_center_x, 0)
    .hole(hinge_diameter)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_spacing)
    .translate((0, 0, base_thickness))
)
result = hinge.union(rib)
result = result.edges("|Z").fillet(fillet_radius)
result = result.edges("|Z").chamfer(chamfer_distance)

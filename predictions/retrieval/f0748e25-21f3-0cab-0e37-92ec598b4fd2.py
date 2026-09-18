import cadquery as cq

plate_length = 80.0
plate_width = 40.0
plate_thickness = 8.0
cup_diameter = 30.0
cup_depth = 4.0
clearance_hole_dia = 6.0
clearance_hole_offset_x = 20.0
clearance_hole_offset_y = 0.0
rib_height = 20.0
rib_thickness = 2.0
rib_extrude = 5.0
fillet_radius = 0.8
chamfer_distance = 1.0

# Base plate with outer vertical chamfers
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_distance)
)
# Recessed cup on front face
base = (
    base.faces(">Y")
    .workplane()
    .center(0, 0)
    .circle(cup_diameter / 2)
    .cutBlind(-cup_depth)
)
# Clearance holes through the plate
hole_positions = [(-clearance_hole_offset_x, clearance_hole_offset_y),
                  (clearance_hole_offset_x, clearance_hole_offset_y)]
base = (
    base.faces(">Y")
    .workplane()
    .pushPoints(hole_positions)
    .hole(clearance_hole_dia)
)
# Thin wall rib extrusion on right side
rib = (
    base.faces(">X")
    .workplane()
    .rect(rib_height, rib_thickness)
    .extrude(rib_extrude)
)
result = base.union(rib)
# Apply a small fillet on a representative edge (lip)
result = result.edges().first().fillet(fillet_radius)

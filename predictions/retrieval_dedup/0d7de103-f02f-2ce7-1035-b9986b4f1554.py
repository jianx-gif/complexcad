import cadquery as cq

base_width = 80.0
base_height = 50.0
plate_thickness = 8.0
inner_cavity_radius = 10.0
rib_thickness = 4.0
rib_height = 30.0
rib_spacing = 12.0
rib_margin = 6.0
rib_depth = 3.0
hole_diameter = 6.0
hole_grid_x = 2
hole_grid_y = 2
hole_pitch_x = 30.0
hole_pitch_y = 20.0
chamfer_distance = 1.0

usable_width = base_width - 2 * rib_margin
rib_count = int(usable_width // rib_spacing) + 1

base_plate = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_distance)
)

plate_with_cavity = (
    base_plate.faces(">Y")
    .workplane()
    .center(-base_width / 4, 0)
    .circle(inner_cavity_radius)
    .cutBlind(-plate_thickness)
)

rib_pockets = (
    plate_with_cavity.faces("<Y")
    .workplane()
    .rarray(rib_spacing, 0, rib_count, 1)
    .rect(rib_thickness, rib_height)
    .cutBlind(-rib_depth)
)

plate_with_ribs = plate_with_cavity.union(rib_pockets)

holes = (
    plate_with_ribs.faces(">Y")
    .workplane()
    .rarray(hole_pitch_x, hole_pitch_y, hole_grid_x, hole_grid_y, center=True)
    .hole(hole_diameter)
)

result = holes

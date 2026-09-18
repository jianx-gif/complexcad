import cadquery as cq

plate_length = 80.0
plate_width = 40.0
plate_thickness = 5.0
bolt_hole_diameter = 5.0
csk_diameter = bolt_hole_diameter * 1.5
csk_depth = plate_thickness
bolt_spacing_x = 50.0
bolt_spacing_y = 20.0
interface_radius = 30.0
chamfer_size = 1.0
rib_width = 5.0
rib_thickness = 3.0
rib_offset = 10.0

# Base loft between plate rectangle and circular interface
base_bracket = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .workplane(offset=plate_thickness)
    .circle(interface_radius)
    .loft(combine=True)
)

# Add reinforcing rib on one side
rib = (
    cq.Workplane("YZ")
    .workplane(offset=-plate_length/2 + rib_offset)
    .rect(rib_width, plate_thickness)
    .extrude(rib_thickness)
)

bracket_with_rib = base_bracket.union(rib)

# Add bolt holes on plate side (bottom face)
bolt_pattern = [
    (-bolt_spacing_x/2, -bolt_spacing_y/2),
    ( bolt_spacing_x/2, -bolt_spacing_y/2),
    (-bolt_spacing_x/2,  bolt_spacing_y/2),
    ( bolt_spacing_x/2,  bolt_spacing_y/2),
]

bracket_with_holes = (
    bracket_with_rib
    .faces("<Z")
    .workplane()
    .pushPoints(bolt_pattern)
    .cskHole(bolt_hole_diameter, csk_diameter, csk_depth)
)

# Apply chamfer to outer edges
result = (
    bracket_with_holes
    .edges("|Z")
    .chamfer(chamfer_size)
)

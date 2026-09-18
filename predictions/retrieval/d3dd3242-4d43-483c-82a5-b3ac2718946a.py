import cadquery as cq

# primary dimensions
case_length = 100.0
case_height = 50.0
case_width_bottom = 80.0
case_width_top = 60.0
wall_thickness = 4.0
base_thickness = 5.0
fillet_radius = 2.0
hole_diameter = 4.0
hole_spacing_x = 20.0
hole_spacing_y = 15.0
hole_rows = 2
hole_cols = 3

# loft parameters
num_steps = 5
step_height = (case_height - base_thickness) / (num_steps - 1)

# generate outer loft profile
first_width = case_width_bottom
first_length = case_length
wp = cq.Workplane("XY").rect(first_length, first_width)
for i in range(1, num_steps):
    t = i / (num_steps - 1)
    width_i = case_width_bottom * (1 - 0.25 * t)  # taper toward top
    length_i = case_length * (1 - 0.15 * t)
    wp = wp.workplane(offset=step_height).rect(length_i, width_i)
case_outer = wp.loft(combine=True)
case_hollow = case_outer.shell(-wall_thickness)

# base plate
base_plate = cq.Workplane("XY").rect(case_length, case_width_bottom).extrude(base_thickness)
result_body = base_plate.union(case_hollow)

# fillet outer vertical edges
result_body = result_body.edges("|Z").fillet(fillet_radius)

# patterned bolt holes on one side (>Y face)
hole_face = result_body.faces(">Y")
result_body = (
    hole_face.workplane(offset=wall_thickness/2)
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows, center=True)
    .hole(hole_diameter)
)
result = result_body

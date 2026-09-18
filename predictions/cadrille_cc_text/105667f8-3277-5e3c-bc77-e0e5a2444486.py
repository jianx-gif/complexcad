import cadquery as cq
overall_width = 80.0
overall_height = 60.0
overall_thickness = 10.0
base_step_width = 50.0
base_step_height = 20.0
base_step_thickness = 5.0
pilot_hole_diameter = 4.0
pilot_hole_offset = 15.0
rib_thickness = 5.0
rib_height = 15.0
rib_count = 6
outer_chamfer = 1.0
inner_fillet_radius = 2.0
base_plate = (
    cq.Workplane("XY")
    .rect(overall_width, overall_height)
    .extrude(base_step_thickness)
)
base_plate = (
    base_plate.faces(">Z")
    .workplane()
    .rect(base_step_width, base_step_height)
    .extrude(base_step_thickness)
)
base_plate = (
    base_plate.faces(">Z")
    .workplane()
    .rect(base_step_width, base_step_height)
    .extrude(base_step_thickness)
)
base_plate = (
    base_plate.faces(">Z")
    .workplane()
    .rect(base_plate_width, base_step_height)
    .extrude(base_step_thickness)
)
base_plate = (
    base_plate.faces(">Z")
    .workplane()
    .rect(overall_width - 2 * pilot_hole_offset, base_step_height - 2 * pilot_hole_offset)
    .rarray(pilot_hole_offset, pilot_hole_offset, pilot_hole_spacing, pilot_hole_spacing)
    .hole(pilot_hole_diameter)
)
rib_count = int((overall_width - 2 * rib_count) // rib_count)
ribs = (
    base_plate.faces(">Z")
    .workplane()
    .pushPoints(rib_count, rib_count)
    .rect(rib_thickness, rib_height)
    .extrude(rib_thickness)
)
result = base_plate.union(ribs)

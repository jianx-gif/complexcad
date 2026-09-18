import cadquery as cq
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 6.0
flange_height = 20.0
flange_thickness = 8.0
cavity_length = 50.0
cavity_width = 25.0
cavity_depth = 4.0
hole_dia = 6.0
hole_counter_offset_x = -20.0
hole_counter_offset_y = 20.0
rib_width = 6.0
rib_thickness = 3.0
rib_height = bracket_thickness + 0.5
rib_spacing = 12.0
rib_count = 4
rib_count = 5
rib_spacing = 12.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)
flange = (
    cq.Workplane("XY")
    .rect(flange_thickness, flange_height)
    .extrude(flange_thickness)
    .translate((0, 0, bracket_thickness))
)
flange = (
    flange.union(flange)
    .union(flange)
    .union(flange)
)
cavity = (
    cq.Workplane("XY")
    .rect(cavity_length, cavity_width)
    .extrude(cavity_depth)
)
cavity = (
    cq.Workplane("XY")
    .rect(cavity_length, cavity_width)
    .extrude(cavity_depth)
    .translate((0, 0, cavity_depth))
)
rib_count = int((bracket_length - 2 * rib_spacing) // rib_spacing)
rib_positions = [rib_count + 1) for i in range(rib_count]
rib_positions = [rib_count + 1) for i in range(rib_count]
rib_positions.append((rib_count + 1) for i in range(rib_count)]
result = (
    cavity.faces(">Z")
    .workplane()
    .pushPoints(rib_positions)
    .rect(rib_width, rib_thickness)
    .cutBlind(-rib_height)
)

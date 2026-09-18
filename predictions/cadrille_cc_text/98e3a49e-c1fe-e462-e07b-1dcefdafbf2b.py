import cadquery as cq
foot_length = 40.0
foot_width = 20.0
foot_height = 20.0
knob_diameter = 30.0
knob_height = 20.0
rib_thickness = 2.0
rib_height = knob_height - 2.0
hole_diameter = 4.0
hole_count = 6
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .rect(foot_length, foot_width)
    .extrude(foot_height)
)
knob_body = (
    base.faces(">Z").workplane()
    .rect(knob_diameter, knob_height)
    .loft()
    .edges("|Z").chamfer(chamfer_distance)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_thickness, foot_width)
    .extrude(rib_height)
    .translate((0, 0, knob_height))
)
result = base.union(rib)
result = (
    result.faces(">Z").workplane()
    .rect(foot_length - 2 * rib_thickness, foot_width - 2 * rib_thickness)
    .extrude(foot_height)
)
result = result.edges("|Z").chamfer(chamfer_distance)
result = (
    result.faces(">Z").workplane()
    .pushPoints([(-hole_count, 0), (hole_count, 0)])
    .hole(hole_diameter)
)
result = (
    result.faces(">Z").workplane()
    .rect(foot_length - 2 * rib_thickness, foot_width - 2 * rib_thickness)
    .extrude(foot_height)
)

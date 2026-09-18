import cadquery as cq

# parameters
arm_base_radius = 15.0
arm_thickness = 5.0
arm_length = 60.0
flange_width = 10.0
flange_thickness = 5.0
blind_hole_diameter = 4.0
blind_hole_depth = 3.5
chamfer_size = 0.8
rib_width = 4.0
rib_height = 3.0
rib_offset_angle = 30.0
slot_height = 20.0
slot_width = arm_thickness + 1.0
slot_depth = 100.0

# revolve arm using a non‑trivial profile directly on a workplane
arm = (
    cq.Workplane("XZ")
    .moveTo(arm_base_radius, 0)
    .lineTo(arm_base_radius + arm_thickness, 0)
    .threePointArc((arm_base_radius + arm_thickness + 2, arm_length/2), (arm_base_radius + arm_thickness, arm_length))
    .lineTo(arm_base_radius, arm_length)
    .close()
    .revolve()
)

# external flange (annular disc) at the base
flange = (
    cq.Workplane("XY")
    .circle(arm_base_radius + flange_width)
    .circle(arm_base_radius)
    .extrude(flange_thickness)
)

# rib for added stiffness, placed on side of arm
rib = (
    cq.Workplane("XZ")
    .rect(rib_width, rib_height)
    .extrude(arm_thickness)
    .rotate((0, 0, 0), (0, 0, 1), rib_offset_angle)
    .translate((arm_base_radius + arm_thickness/2, 0, arm_length/2))
)

# combine core components
result = arm.union(flange).union(rib)

# blind hole in flange top surface (partial depth)
result = (
    result.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .hole(blind_hole_diameter, blind_hole_depth)
)

# side slot cut to relieve stress, defined on the YZ plane intersecting the arm
slot = (
    cq.Workplane("YZ")
    .center(arm_base_radius + arm_thickness/2, arm_length/2)
    .box(slot_width, slot_depth, slot_height)
)
result = result.cut(slot)

# chamfer outer edge of flange
result = result.edges("|Z").chamfer(chamfer_size)

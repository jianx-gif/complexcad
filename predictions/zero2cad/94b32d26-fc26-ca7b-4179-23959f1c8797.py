import cadquery as cq

arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
tab_length = 20.0
tab_width = 30.0
pivot_hole_diameter = 10.0
fillet_radius = 0.8
rib_width = 5.0
rib_height = 3.0
rib_spacing = 15.0
rib_count = int((arm_length - 20) / rib_spacing)

base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)

tab = (
    cq.Workplane("XY")
    .rect(tab_length, tab_width)
    .translate((arm_length/2 + tab_length/2, 0, 0))
    .extrude(arm_thickness)
)

result = base.union(tab)

result = (
    result
    .faces(">Z")
    .workplane()
    .center(arm_length/2, 0)
    .hole(pivot_hole_diameter)
)

result = result.edges().fillet(fillet_radius)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(arm_thickness/2)
)

for i in range(rib_count):
    x_pos = -arm_length/2 + 10 + i * rib_spacing
    result = result.union(
        rib.translate((x_pos, 0, arm_thickness/2))
    )

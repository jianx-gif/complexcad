import cadquery as cq

cap_outer_width = 80.0
cap_outer_height = 80.0
cap_thickness = 20.0
inner_width = 60.0
inner_height = 60.0
rim_chamfer = 2.0
shoulder_fillet = 3.0
mounting_hole_diameter = 5.0
mounting_hole_count = 4
mounting_hole_offset = 5.0
internal_pocket_diameter = 30.0
internal_pocket_depth = 12.0

outer_half_width = cap_outer_width / 2.0
outer_half_height = cap_outer_height / 2.0
inner_half_width = inner_width / 2.0
inner_half_height = inner_height / 2.0
mounting_radius = outer_half_width - mounting_hole_offset

solid = (
    cq.Workplane("XY")
    .box(cap_outer_width, cap_outer_height, cap_thickness)
)

solid = (
    solid
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(inner_width, inner_height)
    .cutBlind(-cap_thickness)
)

solid = (
    solid
    .faces(">Z")
    .workplane()
    .polarArray(radius=mounting_radius, startAngle=0, angle=360, count=mounting_hole_count)
    .hole(mounting_hole_diameter)
)

solid = (
    solid
    .faces("<Z")
    .workplane()
    .center(0, 0)
    .hole(internal_pocket_diameter, depth=internal_pocket_depth)
)

solid = (
    solid
    .edges("|Z and >X")
    .chamfer(rim_chamfer)
)

solid = (
    solid
    .edges("|Z and <X")
    .fillet(shoulder_fillet)
)

result = solid
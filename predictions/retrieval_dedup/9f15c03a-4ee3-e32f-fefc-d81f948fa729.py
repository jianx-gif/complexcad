import cadquery as cq

base_width = 80.0
base_height = 60.0
base_thickness = 4.0
base_corner_radius = 3.0
rib_width = 20.0
rib_length = 40.0
rib_thickness = 2.0
clip_width = 30.0
clip_length = 40.0
clip_thickness = 2.0
clip_margin = 5.0
notch_width = 8.0
notch_height = 5.0
hinge_leg_width = 10.0
hinge_leg_length = 20.0
hinge_leg_thickness = 2.0
pin_bore_diameter = 4.0
chamfer_distance = 1.0
web_height = 6.0
hinge_overlap = 1.0

base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
    .edges("|Z")
    .tag("base_edges")
)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_length)
    .extrude(rib_thickness)
)

clip_profile = (
    cq.Workplane("XY")
    .moveTo(-clip_width/2, -clip_length/2)
    .lineTo(clip_width/2, -clip_length/2)
    .lineTo(clip_width/2, clip_length/4)
    .lineTo(clip_width/4, clip_length/2)
    .lineTo(-clip_width/4, clip_length/2)
    .lineTo(-clip_width/2, clip_length/4)
    .close()
)

clip_body = (
    clip_profile
    .extrude(clip_thickness)
)

clip_with_notch = (
    clip_body
    .faces(">Z")
    .workplane()
    .center(-clip_width/4, -clip_length/4)
    .rect(notch_width, notch_height)
    .cutBlind(notch_height)
)

hinge_leg = (
    cq.Workplane("XY")
    .center(clip_width/2 + hinge_leg_width/2 - hinge_overlap, 0)
    .rect(hinge_leg_width, hinge_leg_length)
    .extrude(hinge_leg_thickness)
)

hinge_up = (
    cq.Workplane("XY")
    .center(clip_width/2 + hinge_leg_width - hinge_overlap, hinge_leg_length - hinge_leg_thickness/2)
    .rect(hinge_leg_thickness, hinge_leg_width)
    .extrude(hinge_leg_thickness)
)

hinge = (
    hinge_leg.union(hinge_up)
    .edges("|Z and >X")
    .chamfer(chamfer_distance)
    .faces(">Z").workplane()
    .center(0, hinge_leg_length - hinge_leg_thickness/2)
    .hole(pin_bore_diameter)
)

web = (
    cq.Workplane("XY")
    .rect(clip_width, web_height)
    .extrude(base_thickness + clip_thickness)
    .translate((0, -base_height/2 + clip_margin, (base_thickness + clip_thickness)/2))
)

assembly = (
    base
    .union(rib.translate((0, 0, base_thickness)))
    .union(clip_with_notch.translate((0, -base_height/2 + clip_margin, base_thickness)))
    .union(hinge.translate((0, -base_height/2 + clip_margin, base_thickness)))
    .union(web)
    .edges(tag='base_edges')
    .fillet(base_corner_radius)
)

result = assembly
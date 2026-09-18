import cadquery as cq

outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
cap_height = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
blind_via_diameter = 10.0
blind_via_depth = 15.0
fillet_radius = 0.2
flange_width = 10.0
flange_thickness = 4.0
rib_count = 6
rib_width = 4.0
rib_height = 5.0
thread_hole_diameter = 6.0
thread_hole_depth = 12.0
slot_length = 12.0
slot_width = 3.0
slot_count = 4

# Base solid cap
cap = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(cap_height)
)

# Thin-walled hollow cap
hollow_cap = cap.shell(-wall_thickness)

# External flange
flange = (
    cq.Workplane("XY")
    .circle(outer_radius + flange_width)
    .extrude(flange_thickness)
    .translate((0, 0, -flange_thickness))
)

cap_with_flange = hollow_cap.union(flange)

# Radial ribs
rib_angle = 360.0 / rib_count
ribs = cq.Workplane("XY")
for i in range(rib_count):
    rib = (
        cq.Workplane("XY")
        .rect(rib_width, rib_height)
        .extrude(cap_height)
        .rotate((0, 0, 0), (0, 0, 1), i * rib_angle)
        .translate((outer_radius - rib_width/2.0, 0, 0))
    )
    ribs = ribs.union(rib)

cap_with_ribs = cap_with_flange.union(ribs)

# Blind via on inner top face
cap_with_via = (
    cap_with_ribs
    .faces(">Z")
    .workplane()
    .hole(blind_via_diameter, blind_via_depth)
)

# Fillet inner edge of blind via (apply to edges on top face)
cap_fillet = cap_with_via.faces(">Z").edges().fillet(fillet_radius)

# Threaded hole on side
threaded = (
    cap_fillet
    .faces("<X")
    .workplane()
    .hole(thread_hole_diameter, thread_hole_depth)
)

# Perimeter clearance slots
slots = cq.Workplane("XY")
slot_angle = 360.0 / slot_count
for i in range(slot_count):
    slot = (
        cq.Workplane("XY")
        .rect(slot_width, slot_length)
        .extrude(cap_height/2)
        .rotate((0,0,0), (0,0,1), i * slot_angle)
        .translate((outer_radius - wall_thickness/2.0, 0, cap_height/4))
    )
    slots = slots.union(slot)

result = threaded.cut(slots)

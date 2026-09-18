import cadquery as cq

outer_radius = 30
cap_height = 20
lip_height = 5
wall_thickness = 2
base_fillet_radius = 3
rib_thickness = 3
rib_depth = wall_thickness - 0.4
rib_height = 12
rib_count = 6

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cap_height)
    .lineTo(outer_radius - lip_height, cap_height + lip_height)
    .lineTo(0, cap_height + lip_height)
    .close()
    .wire()
)

cap = profile.revolve()

cap_shell = cap.shell(-wall_thickness)

cap_fillet = cap_shell.faces("<Z").edges().fillet(base_fillet_radius)

inner_radius = outer_radius - wall_thickness

rib_union = cq.Workplane("XY")
for i in range(rib_count):
    angle = i * 360 / rib_count
    rib = (
        cq.Workplane("XZ")
        .transformed(offset=(inner_radius - rib_depth/2, 0, wall_thickness + rib_height/2))
        .rect(rib_depth, rib_height)
        .extrude(rib_thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    rib_union = rib_union.union(rib)

result = cap_fillet.union(rib_union)

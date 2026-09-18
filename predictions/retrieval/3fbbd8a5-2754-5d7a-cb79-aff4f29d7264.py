import cadquery as cq

# Parameters (units: 1 unit = 0.1 mm)
inner_radius = 10.0
hole_diameter = 13.0
outer_radius = 20.0
flange_height = 5.0
rim_radius = 2.0
cap_height = 30.0
fillet_rad = 0.6
rib_width = 4.0
rib_height = 12.0
rib_thickness = 2.0
mount_tab_width = 12.0
mount_tab_height = 4.0
mount_tab_thickness = 3.0

# 2D profile on XZ plane for revolve – includes built‑in fillet at the outer top corner
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, cap_height - flange_height)
    .threePointArc((outer_radius, cap_height - flange_height/2), (outer_radius, cap_height))
    .lineTo(outer_radius, cap_height + flange_height)
    .threePointArc(
        (outer_radius + fillet_rad, cap_height + flange_height + fillet_rad),
        (outer_radius + rim_radius, cap_height + flange_height)
    )
    .lineTo(outer_radius + rim_radius, 0)
    .close()
)

# Revolve profile around Z axis to create the cap
cap = profile.revolve()

# Clearance hole through the cap (centered on axis)
cap = (
    cap.faces("<Z")
    .workplane()
    .hole(hole_diameter)
)

# Internal ribs for stiffness, placed radially around inner cavity
rib_base = (
    cq.Workplane("XY")
    .center(inner_radius + (outer_radius - inner_radius) / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

rib0 = rib_base
rib120 = rib_base.rotate((0, 0, 0), (0, 0, 1), 120)
rib240 = rib_base.rotate((0, 0, 0), (0, 0, 1), 240)

cap = cap.union(rib0).union(rib120).union(rib240)

# Mounting tab on outer face for attachment – penetrates the cap to ensure a single solid
mount_tab = (
    cq.Workplane("XY")
    .center(outer_radius + rim_radius - mount_tab_thickness/2.0, 0)
    .rect(mount_tab_thickness, mount_tab_width)
    .extrude(mount_tab_height)
    .translate((0, 0, cap_height/2.0 - mount_tab_height/2.0))
)

result = cap.union(mount_tab)

import cadquery as cq

# Parameters
max_dim = 100.0

total_length = 80.0
body_radius = 20.0
inlet_outer_radius = 25.0
inlet_length = 15.0
body_cyl_length = 40.0
outlet_counterbore_radius = 12.0
outlet_counterbore_depth = 10.0
flange_radius = 30.0
flange_thickness = 5.0

inner_inlet_radius = 10.0
inner_body_radius = 8.0
inner_counterbore_radius = 9.0

mount_hole_dia = 6.0
mount_hole_radius = flange_radius - 10.0
mount_hole_count = 4

chamfer_dist = 1.0
rib_thickness = 2.0
rib_height = 5.0

# Outer profile sketch on XZ plane
outer_profile = (
    cq.Workplane('XZ')
    .moveTo(inlet_outer_radius, 0)
    .lineTo(body_radius, inlet_length)
    .lineTo(body_radius, inlet_length + body_cyl_length)
    .lineTo(outlet_counterbore_radius, total_length - outlet_counterbore_depth - flange_thickness)
    .lineTo(outlet_counterbore_radius, total_length - flange_thickness)
    .lineTo(flange_radius, total_length - flange_thickness)
    .lineTo(flange_radius, total_length)
    .close()
)

outer_body = outer_profile.revolve()
outer_body = outer_body.edges().chamfer(chamfer_dist)

# Inner bore profile
inner_profile = (
    cq.Workplane('XZ')
    .moveTo(inner_inlet_radius, 0)
    .lineTo(inner_body_radius, inlet_length)
    .lineTo(inner_body_radius, inlet_length + body_cyl_length)
    .lineTo(inner_counterbore_radius, total_length - outlet_counterbore_depth - flange_thickness)
    .lineTo(inner_counterbore_radius, total_length - flange_thickness)
    .close()
)

inner_cutter = inner_profile.revolve()

valve_body = outer_body.cut(inner_cutter)

# Counterbore at outlet (from top flange)
valve_body = (
    valve_body
    .faces(">Z")
    .workplane(offset=-flange_thickness)
    .hole(outlet_counterbore_radius * 2, outlet_counterbore_depth)
)

# Mounting holes on flange (circular pattern)
valve_body = (
    valve_body
    .workplane(offset=total_length)
    .polarArray(mount_hole_radius, 0, 360, mount_hole_count)
    .hole(mount_hole_dia)
)

# Inspection pocket on side (+Y direction)
valve_body = (
    valve_body
    .faces(">Y")
    .workplane()
    .rect(30.0, 10.0)
    .cutBlind(-5.0)
)

# Reinforcing rib added by union of a rectangular block positioned on side
rib = (
    cq.Workplane('XY')
    .box(rib_thickness, body_cyl_length, rib_height)
    .translate((body_radius + rib_thickness/2, 0, inlet_length + body_cyl_length/2))
)

valve_body = valve_body.union(rib)

result = valve_body
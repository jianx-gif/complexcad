import cadquery as cq

# Parameters
height = 80.0
radius_bottom = 40.0
radius_top = 25.0
fillet_radius = 2.0
vent_slot_width = 5.0
vent_slot_length = 30.0
vent_slot_spacing = 10.0
vent_grid_width = 40.0
vent_grid_height = 50.0
chamfer_size = 1.0
mount_hole_diameter = 6.0
mount_hole_spacing = 30.0
counterbore_diameter = 12.0
counterbore_depth = 4.0
rib_thickness = 4.0
rib_height = height * 0.8

# Base lofted block
base = (
    cq.Workplane("XY")
    .circle(radius_bottom)
    .workplane(offset=height)
    .circle(radius_top)
    .loft()
)

# Fillet top and bottom circular edges
base_fillet = (
    base.faces(">Z").edges().fillet(fillet_radius)
    .faces("<Z").edges().fillet(fillet_radius)
)

# Compute vent array counts
num_slots_x = int(vent_grid_width // vent_slot_spacing)
num_slots_y = int(vent_grid_height // vent_slot_spacing)

# Vent cutting tool
vent = (
    cq.Workplane()
    .transformed(offset=(radius_bottom - 0.01, 0, height / 2.0), rotate=(0, 90, 0))
    .rect(vent_slot_width, vent_slot_length)
    .rarray(vent_slot_spacing, vent_slot_spacing, num_slots_x, num_slots_y, center=True)
    .extrude(radius_bottom * 2 + 0.02)
    .chamfer(chamfer_size)
)

# Subtract vent from body
body_with_vent = base_fillet.cut(vent)

# Add counterbored mounting holes on top surface
top_holes = (
    body_with_vent.faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing / 2, 0), (mount_hole_spacing / 2, 0)])
    .cboreHole(mount_hole_diameter, counterbore_diameter, counterbore_depth)
)

# Add internal reinforcing rib (vertical plate) centered in Y
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(radius_bottom * 2)
    .translate((0, 0, height * 0.1))
)

# Combine all features into final result
result = top_holes.union(rib)

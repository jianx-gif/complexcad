import cadquery as cq

# Parameters
flange_thickness = 8.0
arm_length = 80.0
mid_section_length = 30.0
base_diameter = 30.0
mid_diameter = 20.0
tip_diameter = 10.0
mount_flange_diameter = 70.0
fillet_radius = 5.0
pilot_hole_diameter = 4.0
pilot_hole_offset = 55.0
mount_hole_diameter = 6.0
mount_hole_spacing = 30.0

# Derived radii
flange_radius = mount_flange_diameter / 2.0
base_radius = base_diameter / 2.0
mid_radius = mid_diameter / 2.0
tip_radius = tip_diameter / 2.0

# Profile for revolved arm with flange
profile = (
    cq.Workplane("XZ")
    .polyline([
        (flange_radius, 0),
        (base_radius, flange_thickness),
        (mid_radius, flange_thickness + mid_section_length),
        (tip_radius, arm_length),
        (0, arm_length),
    ])
    .close()
    .revolve()
)

# Apply global fillet
result = profile.fillet(fillet_radius)

# Mounting holes on flange (through the base face)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)

# Pilot hole perpendicular to arm axis at specified offset
pilot_cylinder = (
    cq.Workplane("YZ")
    .center(pilot_hole_offset, 0)  # (Z, Y) in YZ plane
    .circle(pilot_hole_diameter/2)
    .extrude(flange_radius*2 + 20)
)
result = result.cut(pilot_cylinder)

# Stiffening rib attached to outer surface midway along arm
rib_width = 5.0
rib_height = 3.0
rib_length = 20.0
rib = (
    cq.Workplane("XZ")
    .center(mid_radius + rib_width/2, flange_thickness + mid_section_length/2)
    .rect(rib_width, rib_height)
    .extrude(rib_length)
)
result = result.union(rib)

# Additional pocket on side for weight reduction
pocket = (
    cq.Workplane("XZ")
    .center(mid_radius - 2, flange_thickness + mid_section_length/4)
    .rect(4, 12)
    .extrude(rib_length)
)
result = result.cut(pocket)

import cadquery as cq

# Parameters
outer_diameter = 100.0
inner_diameter = 20.0
hub_radius = 12.0
hub_height = 8.0
disk_thickness = 10.0
shell_thickness = 2.0
rim_fillet_radius = 1.5
blade_length = 30.0
blade_width = 5.0
blade_thickness = 2.0
blade_fillet = 0.5
num_blades = 6
oil_channel_width = 4.0

# Base outer cylinder and thin-walled shell
outer_cyl = cq.Workplane("XY").circle(outer_diameter/2).extrude(disk_thickness)
shelled = outer_cyl.shell(-shell_thickness)

# Central hub
hub = cq.Workplane("XY").circle(hub_radius).extrude(hub_height)

# Combine hub with shelled disk
base = shelled.union(hub)

# Blade geometry (rectangular blade with filleted leading edge)
blade_center_x = hub_radius + blade_length/2
blade = (
    cq.Workplane("XY")
    .center(blade_center_x, 0)
    .rect(blade_length, blade_width)
    .extrude(disk_thickness)
    .edges("|Y")
    .fillet(blade_fillet)
)

# Replicate blades around the axis
blades = cq.Workplane("XY")
for i in range(num_blades):
    angle = i * 360.0 / num_blades
    blades = blades.union(blade.rotate((0, 0, 0), (0, 0, 1), angle))

# Add blades to the base part
base = base.union(blades)

# Oil passage: radial rectangular channel cut through hub to outer rim
oil_channel = (
    cq.Workplane("XY")
    .center((hub_radius + outer_diameter/2)/2, 0)
    .rect(oil_channel_width, disk_thickness + 2*shell_thickness)
    .extrude(disk_thickness)
)
base = base.cut(oil_channel)

# Fillet outer rim edges for safety
result = base.edges("|Z").fillet(rim_fillet_radius)

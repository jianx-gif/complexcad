import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 20.0
arm_thickness = 8.0
tab_width = 30.0
tab_height = 12.0
cable_hole_diameter = 4.0
cable_hole_offset = 5.0
mount_hole_diameter = 3.0
mount_hole_offset = 10.0
slot_width = 6.0
slot_length = arm_length * 0.3
rib_width = 6.0
rib_length = arm_length * 0.6
rib_height = arm_thickness * 0.5
chamfer_size = 0.8

# Base lever arm
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)

# Integrated tab
tab = (
    cq.Workplane("XY")
    .center(arm_length / 2 + tab_width / 2, 0)
    .rect(tab_width, tab_height)
    .extrude(arm_thickness)
)

lever = base.union(tab)

# Cable tie through‑hole on tab
lever = (
    lever
    .faces(">Z")
    .workplane()
    .center(arm_length / 2 + tab_width / 2 - cable_hole_offset, 0)
    .hole(cable_hole_diameter)
)

# Mounting holes on lever arm (two symmetric)
lever = (
    lever
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-arm_length / 2 + mount_hole_offset, arm_width / 2 - mount_hole_offset),
        (-arm_length / 2 + mount_hole_offset, -arm_width / 2 + mount_hole_offset),
    ])
    .hole(mount_hole_diameter)
)

# Weight‑reducing slot near root
lever = (
    lever
    .faces(">Z")
    .workplane()
    .center(-arm_length * 0.25, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-arm_thickness / 2)
)

# Stiffening rib on back side
rib = (
    cq.Workplane("XY")
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .translate((0, 0, -rib_height))
)
lever = lever.union(rib)

# Chamfer top perimeter edges
lever = lever.faces(">Z").edges().chamfer(chamfer_size)

result = lever
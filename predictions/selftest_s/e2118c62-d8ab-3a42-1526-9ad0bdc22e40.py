import cadquery as cq

# Parameters
outer_radius = 30
block_length = 50
clearance_slot_width = 10
clearance_slot_depth = 12
keyway_width = 6
keyway_depth = 8
fillet_radius = 2
mount_hole_diameter = 5
mount_hole_offset = 18
rib_height = 6
rib_width = 8
rib_thickness = 3

# Base profile sketch on XZ plane (revolve around Z)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, block_length)
    .lineTo(outer_radius, block_length)
    .lineTo(outer_radius, 0)
    .close()
)
result = profile.revolve()
# Fillet outer rim edge (top perimeter)
result = result.edges(">Z").fillet(fillet_radius)
# Central clearance slot (axial rectangular cut)
slot = (
    cq.Workplane("XY")
    .box(clearance_slot_width, block_length + 2, clearance_slot_depth)
    .translate((outer_radius - clearance_slot_depth / 2, 0, 0))
)
result = result.cut(slot)
# Recessed keyway inside the clearance slot
keyway = (
    cq.Workplane("XY")
    .box(keyway_width, block_length + 2, keyway_depth)
    .translate((outer_radius - clearance_slot_depth - keyway_depth / 2, 0, 0))
)
result = result.cut(keyway)
# Mounting holes on top face
result = (
    result.faces(">Z")
    .workplane()
    .center(mount_hole_offset, 0)
    .hole(mount_hole_diameter)
    .center(-mount_hole_offset, 0)
    .hole(mount_hole_diameter)
)
# Mounting holes on bottom face
result = (
    result.faces("<Z")
    .workplane()
    .center(mount_hole_offset, 0)
    .hole(mount_hole_diameter)
    .center(-mount_hole_offset, 0)
    .hole(mount_hole_diameter)
)
# Stiffening ribs placed just inside the clearance slot
rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_width, rib_height)
    .translate((outer_radius - clearance_slot_depth - rib_thickness / 2, 0, block_length / 2))
)
result = result.union(rib)
# Mirror rib to opposite side across YZ plane
rib_mirror = rib.mirror(mirrorPlane="YZ")
result = result.union(rib_mirror)

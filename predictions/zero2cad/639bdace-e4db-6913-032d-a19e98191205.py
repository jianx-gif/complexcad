import cadquery as cq

# Parameters
hub_radius = 20.0
hub_length = 30.0
flange_radius = 30.0
flange_thickness = 8.0
keyway_width = 6.0
keyway_depth = 4.0
keyway_length = 20.0
chamfer_size = 1.5
mount_hole_dia = 5.0
mount_hole_spacing = 20.0
mount_hole_offset = 10.0
pocket_width = 12.0
pocket_height = 6.0
pocket_depth = 4.0

# Base hub profile and revolve
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(hub_radius, 0)
    .lineTo(hub_radius, hub_length)
    .lineTo(flange_radius, hub_length)
    .lineTo(flange_radius, hub_length + flange_thickness)
    .lineTo(0, hub_length + flange_thickness)
    .close()
)
result = profile.revolve()

# Keyway cut (rectangular slot on outer flange)
keyway = (
    cq.Workplane("XY")
    .center(flange_radius - keyway_depth / 2, hub_length + flange_thickness / 2)
    .rect(keyway_width, keyway_length)
    .extrude(keyway_depth)
)
result = result.cut(keyway)

# Mounting holes on flange (four-hole rectangular pattern)
hole_positions = [
    (mount_hole_offset, mount_hole_spacing / 2),
    (-mount_hole_offset, mount_hole_spacing / 2),
    (mount_hole_offset, -mount_hole_spacing / 2),
    (-mount_hole_offset, -mount_hole_spacing / 2),
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_dia)
)

# Chamfer on outer flange edge (top circular edge)
result = result.edges(">Z").chamfer(chamfer_size)

# Pocket on outer flange for weight reduction
result = (
    result.faces(">Z")
    .workplane()
    .center(flange_radius - pocket_depth / 2, 0)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)

# Internal rib for stiffness (cylindrical rib inside hub)
rib_radius = hub_radius - 5.0
rib_height = hub_length - 5.0
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(rib_radius)
    .extrude(rib_height)
    .translate((0, 0, 2.5))
)
result = result.union(rib)

# Small fillet on inner hub transition for safety
result = result.edges("|Z").fillet(0.8)

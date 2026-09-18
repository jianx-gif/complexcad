import cadquery as cq

# Parameter definitions
outer_diameter = 80.0
inner_diameter = 40.0
plate_thickness = 8.0
central_hole_diameter = 20.0
fillet_radius = 2.0
rib_height = 3.0
rib_width = 6.0
rib_count = 8
boss_diameter = 12.0
boss_height = 5.0
slot_width = 4.0
slot_depth = 2.0
slot_depth_z = 4.0

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
boss_radius = boss_diameter / 2.0

# Base profile for revolve on XZ plane (stepped shape)
profile = (
    cq.Workplane('XZ')
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, plate_thickness)
    .lineTo(inner_radius, plate_thickness)
    .lineTo(inner_radius, 0)
    .close()
)

# Revolve to create washer solid
washer = profile.revolve()

# Central clearance hole (through entire thickness)
washer = washer.faces('>Z').workplane().hole(central_hole_diameter)

# Boss cutout centered on the central hole, extending radially outward
washer = (
    washer
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .circle(boss_radius)
    .cutBlind(boss_height)
)

# Fillet on all suitable edges (inner and outer walls, top/bottom)
washer = washer.edges().fillet(fillet_radius)

# Create a single rib solid and array it around Z
base_rib = (
    cq.Workplane('XY')
    .box(rib_width, rib_height, plate_thickness)
    .translate((outer_radius + rib_height/2, 0, 0))
)

ribs = base_rib
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    ribs = ribs.union(base_rib.rotate((0, 0, 0), (0, 0, 1), angle))

washer = washer.union(ribs)

# Rectangular slot on inner cylindrical face for tool clearance
slot_solid = (
    cq.Workplane('XY')
    .box(slot_width, slot_depth, plate_thickness)
    .translate((inner_radius/2, 0, 0))
)
washer = washer.cut(slot_solid)

result = washer

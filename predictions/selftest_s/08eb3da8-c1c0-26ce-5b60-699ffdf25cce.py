import cadquery as cq

# Primary dimensions
hub_length = 30
shaft_length = 20
shoulder_length = 10
bore_radius = 8
shoulder_radius = 12
hub_radius = 20

# Tab geometry
tab_length = 15
tab_width = 8
tab_height = 6
tab_fillet_radius = 1
tab_overlap = 0.3
num_tabs = 4

# Chamfer and slot details
chamfer_distance = 0.5
slot_width = 6
slot_depth = 5

# Bolt hole for tabs
tab_hole_diameter = 3

# Derived parameters
total_length = shaft_length + shoulder_length + hub_length
tab_center_radius = hub_radius + tab_length / 2 - tab_overlap

# Hub core created by revolving a profile
hub = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(bore_radius, 0)
    .lineTo(bore_radius, shaft_length)
    .lineTo(shoulder_radius, shaft_length)
    .lineTo(shoulder_radius, shaft_length + shoulder_length)
    .lineTo(hub_radius, shaft_length + shoulder_length)
    .lineTo(hub_radius, shaft_length + shoulder_length + hub_length)
    .lineTo(0, shaft_length + shoulder_length + hub_length)
    .close()
    .revolve()
)

# Remove central bore through full length
bore = cq.Workplane("XY").circle(bore_radius).extrude(total_length)
hub = hub.cut(bore)

# Add chamfer on the outermost cylindrical face
hub = hub.faces(">Z").edges().chamfer(chamfer_distance)

# Cut a rectangular slot on the positive X side of the hub shoulder
slot = (
    hub.faces(">X").first()
    .workplane()
    .center(0, shaft_length + shoulder_length / 2)
    .rect(slot_width, slot_depth)
    .cutBlind(- (hub_radius - bore_radius))
)

# Create tabs positioned at middle of shoulder height
tab_plane = cq.Workplane("XY").transformed(offset=(0, 0, shaft_length + shoulder_length / 2))

tab_profile = (
    tab_plane
    .rect(tab_length, tab_width)
    .polarArray(count=num_tabs, startAngle=0, angle=360, radius=tab_center_radius)
)

tabs = tab_profile.extrude(tab_height).edges("|Z").fillet(tab_fillet_radius)

# Union hub and tabs
result = hub.union(tabs)

# Drill clearance holes through each tab
hole_pattern = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, shaft_length + shoulder_length / 2))
    .circle(tab_hole_diameter / 2)
    .polarArray(count=num_tabs, startAngle=0, angle=360, radius=tab_center_radius)
)
result = result.cut(hole_pattern.extrude(-tab_height))

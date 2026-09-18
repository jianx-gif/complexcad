import cadquery as cq
outer_radius = 45
hub_radius = 15
base_thickness = 5
hub_radius = hub_radius + 2
front_thickness = 2
socket_diameter = 16
socket_depth = 8
bolt_diameter = 16
bolt_circle_radius = 18
bolt_circle_radius = 17
bolt_count = 8
bolt_angle = 60
bolt_count = 12
bolt_depth = base_thickness + 0.5
vent_diameter = 4
vent_rows = 2
vent_cols = 3
vent_spacing = 4
vent_rows = 3
vent_cols = 4
outer_radius = outer_radius - 2 * outer_radius
inner_radius = outer_radius - 2 * outer_radius
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(base_thickness)
)
front = base.faces(">Z").edges().chamfer(front_thickness)
bolt = (
    cq.Workplane("XY")
    .circle(bolt_circle_radius)
    .extrude(bolt_depth)
)
bolt = (
    cq.Workplane("XY")
    .circle(bolt_circle_radius)
    .extrude(bolt_depth)
)
bolt = bolt.cut(bolt)
bolt = bolt.edges("|Z").chamfer(bolt_depth)
bolt = bolt.faces(">Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.cut(bolt)
bolt = bolt.faces(">Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.faces(">Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.faces(">Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.faces(">Z").edges().chamfer(bolt_depth)
bolt = bolt.faces("<Z").edges().fillet(0.5)
bolt = bolt.faces("<Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.faces("<Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.faces("<Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.faces("<Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.faces("<Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.faces("<Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.faces("<Z").edges().chamfer(bolt_depth)
bolt = bolt.faces("<Z").edges().fillet(0.5)
bolt = bolt.faces("<Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.edges().chamfer(bolt)
bolt = bolt.faces("<Z").edges().chamfer(bolt_depth)
bolt = bolt.faces(">Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.cut(bolt)
bolt = bolt.faces("<Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.cut(bolt)
bolt = bolt.faces("<Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt.faces("<Z").workplane().center(0, 0).circle(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt
bolt = bolt.faces("<Z").workplane().center(0, 0).rect(bolt_circle_radius).extrude(bolt_depth)
bolt = bolt
bolt = bolt
bolt = bolt
bolt = bolt
bolt = bolt
bolt = bolt
bolt = bolt
bolt = bolt
bolt =
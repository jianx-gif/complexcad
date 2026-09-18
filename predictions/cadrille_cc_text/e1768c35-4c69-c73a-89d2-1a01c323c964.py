import cadquery as cq
import math
elbow_angle_deg = 120.0
elbow_angle_deg = 45.0
elbow_angle_rad = math.radians(elbow_angle_deg)
elbow_radius = 25.0
wall_thickness = 3.0
chamfer_size = 1.0
bolt_diameter = 12.7
bolt_hole_diameter = 5.0
bolt_spacing = 10.0
bolt_angle_rad = 45.0
bolt_angle_deg = 45.0
rib_thickness = 1.0
rib_height = wall_thickness + 2.0
rib_length = wall_thickness + 2.0
pocket_depth = 2.0
pocket_width = 8.0
pocket_depth = 2.0
pocket_margin = 10.0
base = (
    cq.Workplane("XY")
    .circle(elbow_radius)
    .extrude(elbow_angle_rad)
    .translate((0, 0, elbow_angle_rad))
)
base = base.cut(base)
rib = (
    cq.Workplane("XY")
    .circle(rib_length)
    .extrude(rib_height)
    .translate((0, 0, rib_length))
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_size)
hole_positions = [(-bolt_angle_rad/2, 0), (bolt_angle_rad/2, 0)]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(bolt_diameter/2)
    .cutBlind(-bolt_angle_rad)
)
base = base.edges(">Z").chamfer(chamfer_size)
result = base

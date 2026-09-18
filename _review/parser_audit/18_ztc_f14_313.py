import cadquery as cq
import math
plate_diameter = 80.0
plate_thickness = 5.0
outer_fillet_radius = 2.0
edge_chamfer = 0.5
recess_diameter = 30.0
recess_depth = 2.0
slot_length = 20.0
slot_width = 5.0
slot_radius = 2.5
slot_count = 12
slot_radius_from_center = plate_diameter/2 - slot_length/2 - 5.0
mounting_hole_dia = 4.0
mounting_hole_depth = 2.0
rib_height = 1.0
rib_thickness = 2.0
rib_count = 6
# Base plate creation
result = cq.Workplane("XY").circle(plate_diameter/2).extrude(plate_thickness)
result = result.faces(">Z").edges().fillet(outer_fillet_radius)
result = result.faces("<Z").edges().chamfer(edge_chamfer)
result = result.faces(">Z").workplane().circle(recess_diameter/2).cutBlind(-recess_depth)
# Compute slot centers around perimeter
slot_centers = []
for i in range(slot_count):
    ang = math.radians(i * 360.0 / slot_count)
    x = slot_radius_from_center * math.cos(ang)
    y = slot_radius_from_center * math.sin(ang)
    slot_centers.append((x, y))
# Cut slots through full thickness
result = result.workplane().pushPoints(slot_centers).slot2D(slot_length, slot_width, slot_radius).cutThruAll()
# Add clearance holes at slot centers
result = result.workplane().pushPoints(slot_centers).hole(mounting_hole_dia, mounting_hole_depth)
# Internal ribs radiating outward, placed on bottom face and extending upward
rib_radius = (recess_diameter/2 + plate_diameter/2) / 2
rib_length = (plate_diameter - recess_diameter) / 2 - 5.0
rib_base = result.faces("<Z").workplane().center(rib_radius, 0).rect(rib_thickness, rib_length).extrude(rib_height)
# Create polar array of ribs and fuse with plate
rib_assembly = rib_base
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    rib_assembly = rib_assembly.union(rib_base.rotate((0,0,0), (0,0,1), angle))
result = result.union(rib_assembly)

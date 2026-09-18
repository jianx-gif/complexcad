import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
boss_size = 30.0
boss_height = 6.0
boss_chamfer = 1.0
blind_hole_dia = 5.0
blind_hole_depth = 4.0
hole_offset = 12.0
mounting_hole_dia = 6.0
mounting_hole_offset = 10.0
rib_width = 8.0
rib_thickness = 3.0
rib_height = 2.0
rib_spacing = 15.0
rib_rows = 3
rib_cols = 2
edge_chamfer = 0.5

plate_sketch = cq.Sketch().rect(plate_length, plate_width).circle(boss_size/2, mode='s')
result = cq.Workplane("XY").add(plate_sketch).extrude(plate_thickness)
result = result.faces(">Z").workplane().rect(boss_size, boss_size).extrude(boss_height)
result = result.edges("|Z").chamfer(boss_chamfer)
hole_positions = [(hole_offset, 0), (-hole_offset, 0), (0, hole_offset), (0, -hole_offset)]
result = (result.faces(">Z").workplane()
          .pushPoints(hole_positions)
          .hole(blind_hole_dia, depth=blind_hole_depth))
mount_positions = [( plate_length/2 - mounting_hole_offset,  plate_width/2 - mounting_hole_offset),
                  (-plate_length/2 + mounting_hole_offset,  plate_width/2 - mounting_hole_offset),
                  (-plate_length/2 + mounting_hole_offset, -plate_width/2 + mounting_hole_offset),
                  ( plate_length/2 - mounting_hole_offset, -plate_width/2 + mounting_hole_offset)]
result = (result.faces("<Z").workplane()
          .pushPoints(mount_positions)
          .hole(mounting_hole_dia))
# reinforcement ribs on bottom face
ribs = (cq.Workplane("XY")
        .rarray(rib_spacing, rib_spacing, rib_rows, rib_cols)
        .rect(rib_width, rib_thickness)
        .extrude(rib_height))
# keep only rib material that intersects the plate
ribs = ribs.intersect(result)
result = result.union(ribs)

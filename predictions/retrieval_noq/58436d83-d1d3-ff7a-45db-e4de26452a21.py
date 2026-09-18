import cadquery as cq

outer_width = 80.0
outer_length = 80.0
thickness = 8.0
central_bore_dia = 25.0
inner_fillet_radius = 2.0
slot_width = 6.0
slot_length = 20.0
hole_pitch_radius = 30.0
counterbore_dia = 6.0
counterbore_depth = 3.0
hole_count = 6
chamfer_dist = 1.0
rib_thickness = 2.0
rib_width = 10.0
rib_height = 30.0
boss_dia = 12.0
boss_depth = 4.0

# Base plate
result = cq.Workplane('XY').rect(outer_width, outer_length).extrude(thickness)

# Central bore and inner fillet
result = result.faces('>Z').workplane().hole(central_bore_dia)
result = result.edges('|Z').fillet(inner_fillet_radius)

# Counterbored clearance holes arranged circularly
result = (result.faces('>Z')
          .workplane()
          .circle(hole_pitch_radius)
          .vertices()
          .hole(counterbore_dia, depth=counterbore_depth))

# Outer chamfer before slots (edges are still intact)
result = result.edges('>X or >Y').chamfer(chamfer_dist)

# Side slots for weight reduction
slot_offset_x = outer_width/2 - slot_width/2
result = (result.faces('>Z')
          .workplane()
          .center(-slot_offset_x, 0)
          .rect(slot_width, slot_length)
          .cutBlind(thickness))
result = (result.faces('>Z')
          .workplane()
          .center(slot_offset_x, 0)
          .rect(slot_width, slot_length)
          .cutBlind(thickness))

# Mounting boss on -X side
boss = (cq.Workplane('XY')
        .center(-outer_width/2 + boss_dia, 0)
        .circle(boss_dia/2)
        .extrude(boss_depth))
result = result.union(boss)

# Reinforcing ribs on top surface
rib = (cq.Workplane('XY')
       .rect(rib_width, rib_height)
       .extrude(rib_thickness))
for angle in [0, 90, 180, 270]:
    rib_inst = rib.rotate((0, 0, 0), (0, 0, 1), angle)
    rib_inst = rib_inst.translate((hole_pitch_radius, 0, thickness))
    result = result.union(rib_inst)

# final solid in variable result

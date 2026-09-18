import cadquery as cq
overall_width = 80.0
overall_height = 60.0
overall_thickness = 10.0
base_step_width = 50.0
base_step_height = 20.0
base_step_thickness = 5.0
pilot_hole_diameter = 4.0
pilot_hole_offset = 15.0
inner_fillet_radius = 2.0
outer_chamfer = 1.0
mounting_hole_diameter = 6.0
mounting_hole_spacing = 40.0
rib_thickness = 5.0
rib_height = 15.0
result = (cq.Workplane('XY')
          .rect(overall_width, overall_height)
          .extrude(overall_thickness)
          .faces('<Z')
          .workplane()
          .rect(base_step_width, base_step_height)
          .extrude(base_step_thickness)
          .edges('|Z')
          .fillet(inner_fillet_radius)
          .faces('>Z')
          .workplane()
          .pushPoints([(mounting_hole_spacing/2, 0), (-mounting_hole_spacing/2, 0)])
          .hole(mounting_hole_diameter)
          .faces('>Y')
          .workplane()
          .center(pilot_hole_offset, 0)
          .hole(pilot_hole_diameter)
          .faces('>Z')
          .workplane()
          .rect(rib_thickness, rib_height)
          .translate((overall_width/2 - rib_thickness/2, 0))
          .extrude(rib_thickness)
          .faces('>Z')
          .workplane()
          .rect(rib_thickness, rib_height)
          .translate((-overall_width/2 + rib_thickness/2, 0))
          .extrude(rib_thickness)
          .edges('>Z')
          .chamfer(outer_chamfer)
         )

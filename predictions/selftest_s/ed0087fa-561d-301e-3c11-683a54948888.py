import cadquery as cq
outer_radius = 45
shaft_radius = 15
height = 30
wall_thickness = 5
bearing_pocket_radius = 8
bearing_pocket_depth = 6
blind_hole_radius = 5
blind_hole_depth = 12
chamfer_size = 1.5

wp = cq.Workplane('XZ')
profile = (
    wp.moveTo(shaft_radius, -height/2)
      .lineTo(shaft_radius, -height/4)
      .threePointArc(((shaft_radius+outer_radius)/2, -height/2), (outer_radius, 0))
      .lineTo(outer_radius, height/4)
      .lineTo(outer_radius, height/2)
      .lineTo(shaft_radius, height/2)
      .close()
)
base = profile.revolve()
base = base.edges().chamfer(chamfer_size)
base = base.faces(">Z").workplane().hole(blind_hole_radius, blind_hole_depth)

pocket_center_x = outer_radius - bearing_pocket_depth/2
pocket = (cq.Workplane('XY')
           .center(pocket_center_x, 0)
           .circle(bearing_pocket_radius)
           .extrude(-bearing_pocket_depth))

pocket_mirror = pocket.mirror(mirrorPlane='YZ')
result = base.cut(pocket).cut(pocket_mirror)

import cadquery as cq

plate_length = 80.0
plate_width = 40.0
plate_thickness = 8.0
rib_width = 12.0
spline_offset = 6.0
pin_hole_radius = 4.0
mount_hole_radius = 3.0
pocket_depth = 2.0
chamfer_dist = 1.0

base = cq.Workplane('XY').box(plate_length, plate_width, plate_thickness)
proj_spline_pts = [
    (rib_width + spline_offset, plate_width * 0.25),
    (rib_width + spline_offset, plate_width * 0.75)
]
proj = (
    cq.Workplane('XY')
      .lineTo(rib_width, 0)
      .spline(proj_spline_pts)
      .lineTo(0, plate_width)
      .close()
      .extrude(plate_thickness)
      .translate((plate_length/2, 0, 0))
)
# Fuse with glue to ensure single solid
result = base.union(proj, glue=True)

pin_x = plate_length/2 + rib_width/2
pin_y = 0
result = (
    result.workplane(offset=plate_thickness/2)
          .center(pin_x, pin_y)
          .hole(pin_hole_radius * 2)
)

mount_x = -plate_length/2
mount_y1 = -plate_width/4
mount_y2 = plate_width/4
result = (
    result.workplane(offset=plate_thickness/2)
          .center(mount_x, mount_y1)
          .hole(mount_hole_radius * 2)
)
result = (
    result.workplane(offset=plate_thickness/2)
          .center(mount_x, mount_y2)
          .hole(mount_hole_radius * 2)
)

pocket_w = rib_width / 2
pocket_l = plate_width / 2
result = (
    result.workplane(offset=plate_thickness/2)
          .center(0, 0)
          .rect(pocket_w, pocket_l)
          .cutBlind(-pocket_depth)
)

# Chamfer outer vertical edges
result = result.edges('|Z').chamfer(chamfer_dist)

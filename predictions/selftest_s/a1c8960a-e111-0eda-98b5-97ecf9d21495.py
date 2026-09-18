import cadquery as cq

overall_diameter = 80
overall_thickness = 10
central_hole_diameter = 20
recess_diameter = 30
recess_depth = 4
outer_fillet_radius = 1
mount_hole_diameter = 5
mount_hole_offset_radius = 30
rib_width = 6
rib_height = 4
rib_length = 40
chamfer_distance = 1

base_profile = cq.Sketch()\
    .circle(overall_diameter/2)\
    .circle(central_hole_diameter/2)

base = (cq.Workplane("XY")
    .placeSketch(base_profile)
    .extrude(overall_thickness))

pocket = (base
    .faces(">Z")
    .workplane()
    .circle(recess_diameter/2)
    .cutBlind(recess_depth))

mounts = (pocket
    .faces(">Z")
    .workplane()
    .pushPoints([
        (mount_hole_offset_radius, 0),
        (-mount_hole_offset_radius, 0),
        (0, mount_hole_offset_radius),
        (0, -mount_hole_offset_radius)
    ])
    .hole(mount_hole_diameter))

rib_sketch = cq.Sketch().rect(rib_length, rib_width)

ribs = (mounts
    .faces(">Z")
    .workplane()
    .placeSketch(rib_sketch)
    .extrude(rib_height)
    .rarray(1, 2, 1, 2, center=True)
    .union())

result = (ribs
    .edges("|Z")
    .fillet(outer_fillet_radius)
    .edges()
    .chamfer(chamfer_distance))
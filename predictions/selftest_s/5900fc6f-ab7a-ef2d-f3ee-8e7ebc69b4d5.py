import cadquery as cq

lever_length = 80.0
tri_base = 30.0
tri_height = 20.0
boss_radius = 8.0
boss_length = 20.0
chamfer_len = 2.0
bolt_diameter = 5.0
bolt_counterbore_dia = 9.0
bolt_counterbore_depth = 5.0
hole_offset = 10.0
slot_width = 6.0
slot_length = 30.0

tri_pts = [(-tri_base/2, 0), (tri_base/2, 0), (0, tri_height)]
base = (
    cq.Workplane("YZ")
    .polyline(tri_pts)
    .close()
    .extrude(lever_length)
)

boss = (
    cq.Workplane("YZ")
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_length)
)

part = base.union(boss)
part = part.faces(">X").edges().chamfer(chamfer_len)
part = (
    part.faces(">X")
    .workplane(centerOption="CenterOfMass")
    .hole(bolt_diameter)
    .cskHole(bolt_diameter, bolt_counterbore_dia, bolt_counterbore_depth)
)
part = (
    part.faces(">Y")
    .workplane()
    .center(-hole_offset, 0)
    .hole(bolt_diameter)
    .center(2*hole_offset, 0)
    .hole(bolt_diameter)
)
part = (
    part.faces("<Y")
    .workplane()
    .center(-hole_offset, 0)
    .hole(bolt_diameter)
    .center(2*hole_offset, 0)
    .hole(bolt_diameter)
)
part = (
    part.faces(">Z")
    .workplane()
    .rect(slot_length, slot_width)
    .cutThruAll()
)
result = part
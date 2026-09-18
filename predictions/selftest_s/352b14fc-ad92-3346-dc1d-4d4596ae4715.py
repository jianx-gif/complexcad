import cadquery as cq
from cadquery import Plane

# Parameters
outer_radius = 40.0
length = 80.0
flange_thickness = 8.0
flange_diameter = 70.0
inner_radius_inlet = 12.0
inner_radius_outlet = 6.0
taper_length = 30.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
clip_thickness = 4.0
clip_width = 20.0
clip_height = 6.0
chamfer_size = 1.0

# Base cylinder
base = cq.Workplane('XY').circle(outer_radius).extrude(length)

# Flanges at both ends
flange = cq.Workplane('XY').circle(flange_diameter/2).extrude(flange_thickness)
flange_bottom = flange.translate((0, 0, -flange_thickness))
flange_top = flange.translate((0, 0, length))
part = base.union(flange_bottom).union(flange_top)

# Tapered bore (conical hole) starting from bottom inlet
cone_solid = cq.Solid.makeCone(inner_radius_outlet, inner_radius_inlet, taper_length)
cone = cq.Workplane('XY').add(cone_solid).translate((0, 0, flange_thickness))
part = part.cut(cone)

# Mounting holes on both flanges (4 holes each)
hole_positions = [
    ( mount_hole_spacing/2,  mount_hole_spacing/2),
    (-mount_hole_spacing/2,  mount_hole_spacing/2),
    (-mount_hole_spacing/2, -mount_hole_spacing/2),
    ( mount_hole_spacing/2, -mount_hole_spacing/2)
]
# Bottom flange holes
part = part.faces("<Z").workplane().pushPoints(hole_positions).hole(mount_hole_diameter)
# Top flange holes
part = part.faces(">Z").workplane().pushPoints(hole_positions).hole(mount_hole_diameter)

# Retaining clip tab attached to outer surface near mid length
clip = (
    cq.Workplane('XY')
    .center(outer_radius + clip_thickness/2, length/2)
    .rect(clip_thickness, clip_width)
    .extrude(clip_height)
)
part = part.union(clip)

# Groove for split line (rectangular cut through the body at mid length)
cut_box = cq.Workplane('XY').center(0, length/2).box(outer_radius*2, clip_thickness, length)
part = part.cut(cut_box)

# Chamfer edges on outer cylinder
part = part.edges("|Z").chamfer(chamfer_size)

# Split the part into two halves along the YZ plane (x=0)
result = part.split(Plane.YZ)

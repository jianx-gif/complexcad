import cadquery as cq
import math
gear_teeth = 30
module = 2.0
pressure_angle = 20.0
helix_angle_deg = 30.0
gear_thickness = 15.0
hub_diameter = 20.0
hub_length = 20.0
flange_diameter = 80.0
flange_thickness = 10.0
mount_hole_dia = 5.0
chamfer_size = 0.5

pitch_diameter = module * gear_teeth
pitch_radius = pitch_diameter / 2.0
addendum = module
dedendum = 1.25 * module
root_radius = pitch_radius - dedendum
outer_radius = pitch_radius + addendum

helix_angle_rad = math.radians(helix_angle_deg)
helix_pitch = math.tan(helix_angle_rad) * math.pi * pitch_diameter

base_gear = cq.Workplane("XY").cylinder(gear_thickness, outer_radius)

hub = cq.Workplane("XY").cylinder(hub_length, hub_diameter/2.0).translate((0,0,-(gear_thickness-hub_length)/2))

gear_with_hub = base_gear.union(hub)

# Tooth profile for sweep (rectangular)
tooth_width = (math.pi * module) * 0.5
tooth_height = addendum
profile = (cq.Workplane("YZ")
           .rect(tooth_width, tooth_height)
           .translate((root_radius + tooth_height/2.0, 0, 0)))

helix_wire = cq.Wire.makeHelix(helix_pitch, gear_thickness, root_radius + tooth_height/2.0)

single_tooth_cut = profile.sweep(helix_wire)

# Replicate tooth cut around gear
teeth_cuts = single_tooth_cut
for i in range(1, gear_teeth):
    angle = 360.0 * i / gear_teeth
    rotated = single_tooth_cut.rotate((0,0,0), (0,0,1), angle)
    teeth_cuts = teeth_cuts.union(rotated)

gear_body = gear_with_hub.cut(teeth_cuts)

# Mounting flange
flange = (cq.Workplane("XY")
          .cylinder(flange_thickness, flange_diameter/2.0)
          .translate((0,0,gear_thickness/2.0 + flange_thickness/2.0)))

gear_with_flange = gear_body.union(flange)

# Mounting holes (4-hole pattern) on flange
hole_radius = mount_hole_dia/2.0
hole_offset = flange_diameter/2.0 - 10.0
holes = cq.Workplane("XY")
for i in range(4):
    angle = math.radians(90 * i)
    x = hole_offset * math.cos(angle)
    y = hole_offset * math.sin(angle)
    hole = (cq.Workplane("XY")
            .circle(hole_radius)
            .extrude(flange_thickness + 1)
            .translate((x, y, gear_thickness/2.0 + flange_thickness/2.0)))
    holes = hole if i == 0 else holes.union(hole)

result = gear_with_flange.cut(holes).edges().chamfer(chamfer_size)

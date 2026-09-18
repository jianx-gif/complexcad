import cadquery as cq

# Parameters
overall_diameter = 60.0
overall_length = 30.0
wall_thickness = 2.0
groove_depth = 1.5
groove_width = 2.0
groove_position = 15.0
knurl_pitch = 4.0
knurl_height = 1.0
chamfer_distance = 0.5

def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(overall_length, 0)
    .lineTo(overall_length, overall_diameter/2 - wall_thickness)
    .threePointArc((overall_length/2, overall_diameter/2), (0, overall_diameter/2 - wall_thickness))
    .close()
)

base_body = profile.revolve(360)

groove_cylinder = (
    cq.Workplane("XY")
    .circle((overall_diameter/2) - groove_depth)
    .extrude(groove_width)
    .translate((0, 0, groove_position))
)

body_with_groove = base_body.cut(groove_cylinder)

knob_radius = overall_diameter/2
rib_count = int(360 / knurl_pitch)
first_rib = (
    cq.Workplane("XY")
    .center(knob_radius - wall_thickness/2, 0)
    .rect(knurl_height, knurl_pitch/2)
    .extrude(wall_thickness)
    .translate((0, 0, overall_length/2))
)
knurl_combined = first_rib
for i in range(1, rib_count):
    angle = i * knurl_pitch
    rib = (
        cq.Workplane("XY")
        .center(knob_radius - wall_thickness/2, 0)
        .rect(knurl_height, knurl_pitch/2)
        .extrude(wall_thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .translate((0, 0, overall_length/2))
    )
    knurl_combined = knurl_combined.union(rib)

knurled_body = body_with_groove.union(knurl_combined)

final_part = knurled_body.edges().chamfer(chamfer_distance)

result = final_part
import cadquery as cq
import math

outer_radius = 45.0
inner_radius = 30.0
height = 20.0
wall_thickness = 5.0
bore_diameter_top = 10.0
bore_diameter_bottom = 5.0
bore_depth = 15.0
chamfer_size = 1.0
split_gap = 0.5
hole_diameter = 4.0
hole_pattern_radius = 35.0
hole_count = 6

class SplitCradle:
    def __init__(self):
        pass
    def build_profile(self):
        p = (cq.Workplane("XY")
             .lineTo(outer_radius, 0)
             .threePointArc((outer_radius, height/2), (outer_radius - wall_thickness, height/2))
             .lineTo(inner_radius + wall_thickness, height/2)
             .threePointArc((inner_radius, height/2 + wall_thickness), (inner_radius, height))
             .lineTo(inner_radius, 0)
             .close())
        return p
    def revolve(self, profile):
        return profile.revolve()
    def add_mounting_holes(self, solid):
        points = [(hole_pattern_radius * math.cos(math.radians(a)),
                   hole_pattern_radius * math.sin(math.radians(a)))
                  for a in range(0, 360, int(360/hole_count))]
        holes = cq.Workplane("XY")
        for x, y in points:
            holes = holes.union(cq.Workplane("XY").center(x, y).circle(hole_diameter/2).extrude(height+2))
        return solid.cut(holes)
    def add_tapered_bore(self, solid):
        cone = cq.Solid.makeCone(bore_diameter_top/2, bore_diameter_bottom/2, bore_depth)
        cone = cone.translate((0, 0, bore_depth/2))
        return solid.cut(cone)
    def add_split_seam(self, solid):
        cutter = (cq.Workplane("XZ")
                  .box(split_gap, height+2, 200, centered=(True, False, True)))
        parts = solid.split(cutter, keepBottom=True)
        return parts[0]
    def add_chamfer(self, solid):
        return solid.edges("|Z").chamfer(chamfer_size)
    def model(self):
        profile = self.build_profile()
        solid = self.revolve(profile)
        solid = self.add_mounting_holes(solid)
        solid = self.add_tapered_bore(solid)
        solid = self.add_split_seam(solid)
        solid = self.add_chamfer(solid)
        return solid

result = SplitCradle().model()

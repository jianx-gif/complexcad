import cadquery as cq

# Core dimensions (max 100 units scale)
rotor_outer_radius = 40.0
rotor_inner_radius = 20.0
rotor_height = 30.0
bore_diameter = 8.0
fin_thickness = 3.0
fin_height = 12.0
fin_count = 6
chamfer_distance = 1.0
split_plane = cq.Plane.YZ

class SplitRotor:
    def __init__(self):
        pass

    def build_profile(self):
        wp = cq.Workplane("XY")
        wp = wp.moveTo(rotor_inner_radius, 0)
        wp = wp.lineTo(rotor_inner_radius, rotor_height)
        wp = wp.radiusArc((rotor_outer_radius, rotor_height), rotor_outer_radius - rotor_inner_radius)
        wp = wp.lineTo(rotor_outer_radius, 0)
        wp = wp.close()
        return wp

    def create_body(self):
        profile = self.build_profile()
        body = profile.revolve(360)
        return body

    def add_central_bore(self, solid):
        return solid.hole(bore_diameter)

    def add_cooling_fins(self, solid):
        result = solid
        for i in range(fin_count):
            angle = i * 360.0 / fin_count
            result = (
                result.faces('>Z')
                .workplane()
                .center(rotor_outer_radius - fin_thickness / 2, rotor_height / 2)
                .rotate((0, 0, 0), (0, 0, 1), angle)
                .rect(fin_thickness, fin_height)
                .cutBlind(-fin_height / 2)
            )
        return result

    def apply_chamfer(self, solid):
        return solid.edges().chamfer(chamfer_distance)

    def split_part(self, solid):
        return solid.split(split_plane)

    def build(self):
        body = self.create_body()
        body = self.add_central_bore(body)
        body = self.add_cooling_fins(body)
        body = self.apply_chamfer(body)
        return self.split_part(body)

result = SplitRotor().build()

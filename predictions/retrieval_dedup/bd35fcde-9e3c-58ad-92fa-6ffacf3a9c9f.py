import cadquery as cq

total_height = 80.0
max_radius = 40.0
lip_height = 10.0
wall_height = total_height - lip_height
shell_thickness = 1.0
drain_hole_diameter = 6.0
drain_hole_radius = drain_hole_diameter / 2.0
mount_hole_diameter = 5.0

class OilSump:
    def __init__(self):
        pass
    def build_profile(self):
        wp = cq.Workplane("XZ")
        profile = (
            wp
            .moveTo(0, 0)
            .lineTo(0, wall_height)
            .lineTo(max_radius, total_height)
            .lineTo(max_radius, 0)
            .close()
        )
        return profile
    def create_shell(self):
        solid = self.build_profile().revolve()
        shell = solid.shell(shell_thickness)
        return shell
    def add_drain_hole(self, solid):
        hole_cyl = (
            cq.Workplane("XZ")
            .center(0, 0)
            .cylinder(2 * max_radius, drain_hole_radius)
        )
        return solid.cut(hole_cyl)
    def add_mount_holes(self, solid):
        offset = max_radius - lip_height / 2
        hole_positions = [
            (offset, total_height - lip_height / 2),
            (-offset, total_height - lip_height / 2),
            (0, total_height - lip_height / 4),
            (0, total_height - 3 * lip_height / 4),
        ]
        return (
            solid
            .faces("+Z")
            .workplane()
            .pushPoints(hole_positions)
            .hole(mount_hole_diameter)
        )
    def build(self):
        s = self.create_shell()
        s = self.add_drain_hole(s)
        s = self.add_mount_holes(s)
        return s

result = OilSump().build()

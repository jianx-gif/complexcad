import cadquery as cq

head_diameter = 80.0
head_height = 30.0
wall_thickness = 4.0
split_gap = 2.0
valve_port_diameter = 12.0
valve_port_offset = 20.0

class SplitCylinderHead:
    def __init__(self):
        pass
    def base_head(self):
        return cq.Workplane('XY').circle(head_diameter / 2).extrude(head_height)
    def splitter_sheet(self):
        return (
            cq.Workplane('XZ')
            .rect(head_diameter + 2 * wall_thickness, head_height)
            .extrude(split_gap)
            .translate((0, -split_gap / 2, 0))
        )
    def split_part(self, solid):
        splitter = self.splitter_sheet()
        return solid.split(splitter, keepTop=True, keepBottom=True)
    def bridging_web(self):
        return (
            cq.Workplane('XY')
            .rect(wall_thickness, split_gap + wall_thickness)
            .extrude(head_height)
            .translate((head_diameter / 2 - wall_thickness / 2, 0, 0))
        )
    def internal_cavity(self):
        cavity_radius = (head_diameter / 2) - wall_thickness
        cavity_height = head_height - wall_thickness
        return cq.Workplane('XY').circle(cavity_radius).extrude(cavity_height)
    def valve_port(self, solid):
        return solid.faces('>Z').workplane().center(valve_port_offset, 0).hole(valve_port_diameter)
    def apply_chamfer(self, solid):
        return solid
    def build(self):
        head = self.base_head()
        split_head = self.split_part(head)
        web = self.bridging_web()
        head_with_web = cq.Workplane().add(split_head).union(web)
        cavity = self.internal_cavity()
        split_cavity = self.split_part(cavity)
        head_with_cavity = head_with_web.cut(split_cavity)
        with_valve = self.valve_port(head_with_cavity)
        final = self.apply_chamfer(with_valve)
        return final

result = SplitCylinderHead().build()

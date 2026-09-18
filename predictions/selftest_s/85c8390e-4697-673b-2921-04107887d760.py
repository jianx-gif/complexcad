import cadquery as cq
import math

# Parameters
gear_diameter = 80.0
gear_length = 30.0
tooth_height = 5.0
num_threads = 3
bearing_outer_dia = 40.0
bearing_inner_dia = 20.0
bearing_width = 10.0
cup_thickness = 2.0
cut_width = 4.0
cut_depth = 6.0
cut_spacing_angle = 30.0
chamfer_size = 1.0

class WormGear:
    def __init__(self):
        self.base = None
        self.thread = None
        self.bearing_cup = None
        self.result = None

    def build_base(self):
        self.base = (
            cq.Workplane('XY')
            .circle(gear_diameter / 2)
            .extrude(gear_length)
        )
        return self

    def build_thread(self):
        thread_radius = gear_diameter / 2 + tooth_height
        self.thread = (
            cq.Workplane('XY')
            .circle(thread_radius)
            .twistExtrude(gear_length, 360 * num_threads)
        )
        return self

    def build_bearing_cup(self):
        outer = (
            cq.Workplane('XY')
            .workplane(offset=gear_length - bearing_width)
            .circle(bearing_outer_dia / 2)
            .extrude(bearing_width - cup_thickness)
        )
        inner = (
            cq.Workplane('XY')
            .workplane(offset=gear_length - bearing_width)
            .circle(bearing_inner_dia / 2)
            .extrude(bearing_width - cup_thickness)
        )
        self.bearing_cup = outer.cut(inner)
        return self

    def assemble_and_chamfer(self):
        assembled = self.base.union(self.thread).union(self.bearing_cup)
        self.result = assembled.edges().chamfer(chamfer_size)
        return self

    def apply_patterned_cuts(self):
        radius = gear_diameter / 2 + tooth_height / 2
        self.result = (
            self.result.faces('>Z')
                .workplane()
                .polarArray(radius=radius, startAngle=0, angle=360,
                            count=int(360 / cut_spacing_angle), fill=True)
                .rect(cut_width, cut_depth)
                .cutBlind(-cut_depth)
        )
        return self

    def build(self):
        return (
            self.build_base()
                .build_thread()
                .build_bearing_cup()
                .assemble_and_chamfer()
                .apply_patterned_cuts()
                .result
        )

result = WormGear().build()

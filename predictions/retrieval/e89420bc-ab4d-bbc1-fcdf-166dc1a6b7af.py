import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
shell_thickness = 1.0
rib_height = 4.0
rib_width = 4.0
rib_spacing = 12.0
counterbore_diameter = 12.0
counterbore_depth = 3.0
through_hole_diameter = 6.0
mounting_hole_diameter = 5.0
mounting_hole_offset = 10.0
chamfer_distance = 0.5

base_sketch = (
    cq.Sketch()
    .rect(plate_length, plate_width)
    .push([
        ( plate_length/2 - mounting_hole_offset,  plate_width/2 - mounting_hole_offset),
        (-plate_length/2 + mounting_hole_offset,  plate_width/2 - mounting_hole_offset),
        (-plate_length/2 + mounting_hole_offset, -plate_width/2 + mounting_hole_offset),
        ( plate_length/2 - mounting_hole_offset, -plate_width/2 + mounting_hole_offset)
    ])
    .circle(mounting_hole_diameter/2)
)

solid = (
    cq.Workplane('XY')
    .placeSketch(base_sketch)
    .extrude(plate_thickness)
    .edges('|Z').chamfer(chamfer_distance)
    .shell(-shell_thickness)
)

nx = int((plate_length - 2*mounting_hole_offset) // rib_spacing)
ny = int((plate_width - 2*mounting_hole_offset) // rib_spacing)

ribs = (
    solid.faces('>Z').workplane()
    .rarray(rib_spacing, rib_spacing, nx, ny)
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)

result = (
    ribs
    .faces('>Z').workplane()
    .center(0, 0)
    .hole(counterbore_diameter, depth=counterbore_depth)
    .faces('>Z').workplane()
    .center(0, 0)
    .hole(through_hole_diameter, depth=plate_thickness + rib_height)
)

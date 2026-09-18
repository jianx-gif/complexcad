import cadquery as cq
bellows_length = 70.0
bellows_width = bellows_length
inner_radius = 22.0
wall_thickness = 8.0
groove_axial_length = 6.0
groove_depth = 3.0
chamfer_size = 0.3
mount_hole_diameter = 4.0
mount_hole_count = 6
mount_hole_radius = inner_radius + wall_thickness/2
profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (bellows_length, 0),
        (bellows_length, bellows_width),
        (bellows_length - bellows_length, bellows_width),
        (bellows_length - bellows_length, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length - corrugation_depth, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bellows_width + corrugation_depth),
        (bellows_length, bell
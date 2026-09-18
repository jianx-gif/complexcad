import cadquery as cq
foot_diameter = 60.0
foot_height = 5.0
total_height = 80.0
recess_radius = 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_depth = 15.0
hole_count = 6
hole_radius = foot_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(foot_height, 0)
    .lineTo(foot_height, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height + total_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2.0, foot_height)
    .lineTo(foot_diameter / 2
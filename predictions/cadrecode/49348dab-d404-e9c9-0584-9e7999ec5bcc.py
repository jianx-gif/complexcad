import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-67,-13),(67,-13)).segment((67,8)).segment((61,13)).segment((-62,13)).arc((-64,12),(-67,9)).close().assemble().push([(0,-1)]).circle(7,mode='s').finalize().extrude(-200)
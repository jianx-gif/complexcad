import cadquery as cq
w0=cq.Workplane('YZ',origin=(-55,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-50,-36),(17,-42)).segment((17,-84)).segment((50,-84)).segment((50,-48)).segment((50,-47)).segment((50,36)).segment((-17,42)).segment((-17,84)).segment((-50,84)).segment((-50,48)).segment((-50,47)).close().assemble().finalize().extrude(142).union(w1.sketch().arc((-94,-38),(-1,-50),(94,-38)).segment((93,-38)).arc((-1,-49),(-94,-38)).assemble().finalize().extrude(-167))
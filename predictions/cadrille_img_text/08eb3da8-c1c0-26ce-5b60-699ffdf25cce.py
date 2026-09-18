import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,97,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-67,36),(-61,-40),(-2,-83)).segment((-2,-90)).segment((2,-90)).segment((2,-83)).arc((54,-67),(89,-26)).arc((87,-28),(85,-30)).segment((85,-36)).segment((80,-36)).arc((58,-58),(29,-71)).segment((29,-36)).segment((2,-36)).segment((2,-71)).arc((-28,-58),(-50,-36)).segment((-55,-36)).segment((-55,-30)).arc((-64,0),(-55,30)).segment((-55,36)).close().assemble().finalize().extrude(-194).union(w1.sketch().push([(0,3)]).circle(97).circle(61,mode='s').finalize().extrude(-157))
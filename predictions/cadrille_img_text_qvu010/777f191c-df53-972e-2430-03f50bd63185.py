import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,29,0))
w1=cq.Workplane('ZX',origin=(0,58,0))
r=w0.sketch().circle(92).circle(41,mode='s').finalize().extrude(-21).union(w0.sketch().segment((-70,32),(-35,23)).arc((-51,46),(-32,66)).segment((-59,73)).close().assemble().reset().face(w0.sketch().segment((32,-66),(59,-73)).segment((70,-32)).segment((35,-23)).arc((51,-46),(32,-66)).assemble()).finalize().extrude(30)).union(w1.sketch().arc((-75,50),(-59,58),(-42,63)).segment((-42,80)).arc((-60,68),(-75,50)).assemble().finalize().extrude(-117))
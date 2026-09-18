parts = [base]
parts.append(place(fastener("washer", 'M5', 0), axis=(0, 0, 1), point=(20, 6, 2), seat=1.2, flip=False))
parts.append(place(fastener("screw", 'M5-0.8', 10, 0), axis=(0, 0, 1), point=(20, 6, 2), seat=2.3, flip=False))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 0), axis=(0, 0, 1), point=(20, 6, 2), seat=-2, flip=True))

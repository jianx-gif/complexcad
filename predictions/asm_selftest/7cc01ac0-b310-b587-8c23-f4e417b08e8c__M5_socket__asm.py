parts = [base]
parts.append(place(fastener("washer", 'M5', 0), axis=(0, 0, 1), point=(10, 20, 2.5), seat=2.3, flip=False))
parts.append(place(fastener("screw", 'M5-0.8', 12, 0), axis=(0, 0, 1), point=(10, 20, 2.5), seat=3.4, flip=False))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 0), axis=(0, 0, 1), point=(10, 20, 2.5), seat=-2.5, flip=True))
parts.append(place(fastener("washer", 'M5', 1), axis=(0, 0, 1), point=(70, 20, 2.5), seat=2.5, flip=False))
parts.append(place(fastener("screw", 'M5-0.8', 12, 1), axis=(0, 0, 1), point=(70, 20, 2.5), seat=3.6, flip=False))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 1), axis=(0, 0, 1), point=(70, 20, 2.5), seat=-2.5, flip=True))

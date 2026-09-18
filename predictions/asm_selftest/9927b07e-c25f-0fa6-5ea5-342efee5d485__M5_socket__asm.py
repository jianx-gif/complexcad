parts = [base]
parts.append(place(fastener("washer", 'M5', 0), axis=(0, 0, 1), point=(7.5, 20, 4), seat=3.2, flip=False))
parts.append(place(fastener("screw", 'M5-0.8', 14, 0), axis=(0, 0, 1), point=(7.5, 20, 4), seat=4.3, flip=False))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 0), axis=(0, 0, 1), point=(7.5, 20, 4), seat=-4, flip=True))
parts.append(place(fastener("washer", 'M5', 1), axis=(0, 0, 1), point=(7.5, 50, 4), seat=3.2, flip=False))
parts.append(place(fastener("screw", 'M5-0.8', 14, 1), axis=(0, 0, 1), point=(7.5, 50, 4), seat=4.3, flip=False))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 1), axis=(0, 0, 1), point=(7.5, 50, 4), seat=-4, flip=True))

def set_inclination(self, polygons: dict) -> dict:
    '''
    Расчет и присвоение угла наклона
    :param polygons:
    :return:
    '''
    for polygon in polygons:
        polygon_degress = 0
        neighbor_poligons = [
            (polygon[0], round(polygon[1] + (STEP_DIST['degress'] * 2), 6)),
            (polygon[0], round(polygon[1] - (STEP_DIST['degress'] * 2), 6)),
            (round(polygon[0] + (STEP_DIST['degress'] * 2), 6), polygon[1]),
            (round(polygon[0] - (STEP_DIST['degress'] * 2), 6), polygon[1]),

        ]
        for neighbor_poligon in neighbor_poligons:
            try:
                cur_neighbor = polygons[neighbor_poligon]
                height = abs(polygons[polygon]['elevation'] - cur_neighbor['elevation'])
            except Exception as e:
                print(e)
                continue
            b = STEP_DIST['meters']
            result = math.degrees(math.atan(height / b))
            if result > polygon_degress:
                polygon_degress = result
        polygons[polygon]['inclination'] = polygon_degress
    return polygons
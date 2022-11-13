import json
LAT, LNG = 44.914533, 38.945518  # стартовые координаты
STEP_DIST = 0.004  # шаг в градусах
MAX_SIZE_X, MAX_SIZE_Y = (20000, 20000)  # размер карты,в метрах


def create_polygons(slat, slng):
    polygons = {}
    step = int(STEP_DIST * 1000000 * 2)
    start_lat = int(slat * 1000000)
    start_lng = int(slng * 1000000)
    stop_lat = start_lat + int(step * MAX_SIZE_Y)
    stop_lng = start_lng + int(step * MAX_SIZE_X)
    for lat in range(start_lat, stop_lat, step):
        lat /= 1000000
        for lng in range(start_lng, stop_lng, step):
            lng /= 1000000
            polygons[(lat, lng)] = {
                'x1': lng - STEP_DIST,
                'y1': lat - STEP_DIST,
                'x2': lng + STEP_DIST,
                'y2': lat - STEP_DIST,
                'x3': lng - STEP_DIST,
                'y3': lat + STEP_DIST,
                'x4': lng + STEP_DIST,
                'y4': lat + STEP_DIST,
            }
    return polygons
def save_dataset(data):
    with open('dataset.json', 'w') as f:
        json.dump(data, f)

dataset = create_polygons(LAT, LNG)
save_dataset(dataset)
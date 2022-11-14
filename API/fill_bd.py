import pickle

with open('../backend/polygons/datasets/dataset.pickle', 'rb') as f:
    data = pickle.load(f)
    print(data)
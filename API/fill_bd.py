import pickle

with open('../backend/polygons/datasets/dataset.pickle', 'rb') as f:
    data = pickle.load(f)

with open('../backend/polygons/datasets/dataset2.pickle', 'rb') as f:
    data2 = pickle.load(f)

print(data==data2)
print(1)
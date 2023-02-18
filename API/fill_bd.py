import pickle

with open('../ml/datasets/dataset.pickle', 'rb') as f:
    data = pickle.load(f)

with open('../ml/datasets/dataset2.pickle', 'rb') as f:
    data2 = pickle.load(f)

print(data==data2)
print(1)
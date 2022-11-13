import pickle

with open('dataset.pickle', 'rb') as f:
    data = pickle.load(f)
    print(data)
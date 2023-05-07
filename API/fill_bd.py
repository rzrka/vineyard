import pickle
PATH = '../ml/datasets/nonvineyard3.pickle'

# with open('../ml/datasets/dataset2.pickle', 'rb') as f:
#     data2 = pickle.load(f)


def refill_poligon():
    with open(PATH, 'rb') as f:
        poligons = pickle.load(f)
    for poligon in poligons.values():
        poligon['bdod'] = list(poligon['bdod'].values())[0]
        poligon['cec'] = list(poligon['cec'].values())[0]
        poligon['cfvo'] = list(poligon['cfvo'].values())[0]
        poligon['clay'] = list(poligon['clay'].values())[0]
        poligon['nitrogen'] = list(poligon['nitrogen'].values())[0]
        poligon['ocd'] = list(poligon['ocd'].values())[0]
        poligon['ocs'] = list(poligon['ocs'].values())[0]
        poligon['phh2o'] = list(poligon['phh2o'].values())[0]
        poligon['sand'] = list(poligon['sand'].values())[0]
        poligon['silt'] = list(poligon['silt'].values())[0]
        poligon['soc'] = list(poligon['soc'].values())[0]
    with open(PATH, 'wb') as f:
        pickle.dump(poligons, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(poligons)

def costil():
    with open(PATH, 'rb') as f:
        poligons = pickle.load(f)
    for poligon in poligons.values():
        try:
            del poligon['degress']
        except Exception:
            pass
    with open(PATH, 'wb') as f:
        pickle.dump(poligons, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(poligons)

def stay_class():
    with open(PATH, 'rb') as f:
        poligons = pickle.load(f)
    for poligon in poligons.values():
        poligon['growing'] = False
    with open(PATH, 'wb') as f:
        pickle.dump(poligons, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(poligons)
stay_class()
# costil()
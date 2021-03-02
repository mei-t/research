import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score

MAX_LEN1 = 280
MAX_LEN2 = 203

def count_error(d):
    length = d['sentence_length']
    eror_list = [0 for _ in range(length + 1)]
    index = 0
    for k in d['keys']:
        if len(k) == 1:
            index += 1
        elif k == 'Backspace':
            index -= 1 if index < length else 0
            index = min(length, index)
            eror_list[index] += 1
        elif k == 'ArrowLeft':
            index -= 1 if index < length else 0
        elif k == 'ArrowRight':
            index += 1
    return eror_list

def analize(file_count):
    index = 0
    d = {}
    for i in range(1, file_count + 1):
        file_path = '/Users/meitakahashi/Downloads/data_' + str(i) + '.json'
        with open(file_path, 'r') as f:
            json_dict = json.load(f)
            for key in json_dict:
                if json_dict[key]['name'] != "テスト":
                    d[index] = json_dict[key]
                    index += 1
    
    x = np.array([])
    y = np.array([])
    for key in d:
        # timestamsをリストに変換
        tss = d[key]['timestamps']
        ts = tss.split()
        ts = list(map(int, ts))
        d[key]['timestamps'] = ts
        # print(d[key]['timestamps'])

        # keysをリストに変換
        s = d[key]['keys']
        s = s.replace('   ', ' # ')
        keys = s.split()
        keys = [s.replace('#', ' ') for s in keys]
        d[key]['keys'] = keys
        # print(d[key]['keys'])

        # error_listの取得
        error_list = count_error(d[key])
        # print(error_list)

        ts = np.array(ts).astype(np.float64)
        ts /= np.max(ts)
        ts_mean = np.mean(ts)
        diff1 = MAX_LEN1 - len(ts)
        padding1 = np.full(diff1, ts_mean)

        error_list = np.array(error_list)
        error_mean = np.mean(error_list)
        diff2 = MAX_LEN2 - d[key]['sentence_length']
        padding2 = np.full(diff2, error_mean)

        x = np.append(x, np.concatenate([ts, padding1, error_list, padding2]))
        # if d[key]['anger_fear'] > 0:
        # if d[key]['trust_disgust'] > 0:
        # if d[key]['interest_distraction'] > 0:
        # if d[key]['impression_pessimism'] > 0:
        if d[key]['joy_sadness'] > 0:
            label = 1
        # elif d[key]['anger_fear'] == 0:
        # elif d[key]['trust_disgust'] == 0:
        # elif d[key]['interest_distraction'] == 0:
        # elif d[key]['impression_pessimism'] == 0:
        elif d[key]['joy_sadness'] == 0:
            label = 0
        else:
            label = -1
        y = np.append(y, label)
    x = x.reshape((x.shape[0] // (MAX_LEN1 + MAX_LEN2 + 1), (MAX_LEN1 + MAX_LEN2 + 1)))
    print(x)
    print(x.shape)
    print(y)
    print(y.shape)

    predict(x, y)

def predict(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    sc = StandardScaler()
    sc.fit(x_train)
    x_train_std = sc.transform(x_train)
    x_test_std = sc.transform(x_test)

    model = SVC(kernel='linear', random_state=None) # linear or sigmoid
    model.fit(x_train_std, y_train)
    
    pred_train = model.predict(x_train_std)
    accuracy_train = accuracy_score(y_train, pred_train)
    print('トレーニングデータに対する正答率: %.2f' % accuracy_train)

    pred_test = model.predict(x_test_std)
    accuracy_test = accuracy_score(y_test, pred_test)
    print('テストデータに対する正答率: %.2f' % accuracy_test)

    # グラフ表示
    X = PCA(n_components=2).fit_transform(x)
    clf = SVC(gamma="scale", probability=True)
    clf.fit(X, y)

    support = np.zeros(X.shape[0], dtype="bool")
    support[clf.support_] = True
    # import pdb; pdb.set_trace()

    ax = plt.subplot()
    cm = ListedColormap(["b", "g", "r"])

    ax.scatter(X[~support, 0], X[~support, 1], marker="2", c=y[~support], cmap=cm, alpha=0.5)
    ax.scatter(X[support, 0], X[support, 1], marker=".", c=y[support], cmap=cm)

    # # XX, YY = np.meshgrid(np.arange(-5, 5, 0.025), np.arange(-2, 2, 0.025))
    # XX, YY = np.meshgrid()
    # Z = clf.predict_proba(np.stack([XX.ravel(), YY.ravel()], axis=1))
    # ZZ = np.flip(Z.reshape(XX.shape + (3, )), axis=1)
    # ax.imshow(ZZ, alpha=0.1, aspect="auto")
    # ax.imshow(ZZ, alpha=0.1, aspect="auto", extent=(-5, 5, -2, 2))
    plt.savefig("result.png")

if __name__ == '__main__':
    # iris = datasets.load_iris()
    # x = iris.data[:, [2, 3]]
    # y = iris.target
    # predict(x, y)
    analize(3)
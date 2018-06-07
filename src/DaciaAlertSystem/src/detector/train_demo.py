import argparse
import numpy as np

from datasets import das_v2
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', help='top level directory (containing Dacia)')

    args = parser.parse_args()
    globals().update(vars(args))

    X, Y = das_v2(data_dir)
    X = X.reshape(len(X), -1)

    train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    scaler.fit(train_X)
    train_X = scaler.transform(train_X)
    test_X = scaler.transform(test_X)

    model = LogisticRegression()
    model.fit(train_X, train_Y)
    train_accuracy = model.score(train_X, train_Y)*100.
    test_accuracy = model.score(test_X, test_Y)*100.

    print('%.2f train_accuracy'%train_accuracy)
    print('%.2f test_accuracy'%test_accuracy)

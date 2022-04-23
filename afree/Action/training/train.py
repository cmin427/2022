import pandas as pd
from enum import Enum
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.models import load_model

import matplotlib.pyplot as plt
from keras.callbacks import Callback
import itertools
from sklearn.metrics import confusion_matrix


class Actions(Enum):
    # framewise_recognition.h5
    # squat = 0
    # stand = 1
    # walk = 2
    # wave = 3

    # framewise_recognition_under_scene.h5
    # stand = 0
    # walk = 1
    # operate = 2
    # fall_down = 3
    # run = 4
    
    #CLASS 6개
    stand = 0 # 0 : 그 외
    m_kick = 1 # 1 : 몸통 공격(발차기)
    h_kick = 2 # 2 : 머리 공격(발차기)
    # -----추후 데이터 추가----------
    # m_punch = 3 # 3 : 몸통 공격(주먹)
    # h_paul = 4 # 4 : (반칙)머리 공격(주먹)
    # l_paul = 5 # 5 : (반칙)다리 공격(로우킥)



# Callback class to visialize training progress
class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch':[], 'epoch':[]}
        self.accuracy = {'batch':[], 'epoch':[]}
        self.val_loss = {'batch':[], 'epoch':[]}
        self.val_acc = {'batch':[], 'epoch':[]}

    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))

    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))

    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        if loss_type == 'epoch':
            # val_acc
            plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
            # val_loss
            plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')
        plt.legend(loc="upper right")
        plt.show()


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# load data
raw_data = pd.read_csv('C:\\Users\\min\\Desktop\\project\\A-free\\Action\\training\\merge_data.csv', header=0)
dataset = raw_data.values
X = dataset[:, 0:36].astype(float)
Y = dataset[:, 36]
# X = dataset[0:3289, 0:36].astype(float)  # 실행 데이터 무시
# Y = dataset[0:3289, 36]

# 범주를 숫자로 인코딩
encoder = LabelEncoder()
encoder_Y = encoder.fit_transform(Y)
# print(encoder_Y[0], encoder_Y[900], encoder_Y[1800], encoder_Y[2700])
# encoder_Y = [0]*744 + [1]*722 + [2]*815 + [3]*1008 + [4]*811
encoder_Y = [0]*9378 + [1]*2007 + [2]*462
# one hot 코딩
dummy_Y = np_utils.to_categorical(encoder_Y)

# train test split
X_train, X_test, Y_train, Y_test = train_test_split(X, dummy_Y, test_size=0.1, random_state=9)
# X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,shuffle=True,random_state=1004)
# build keras model
model = Sequential()
model.add(Dense(units=128, input_dim=36,activation='relu'))
# model.add(Dense(units=128,activation='relu',input_shape=(28, 28, 1)))
# model.add(Conv2D(input_shape=(28, 28, 1), filters=64, kernel_size=5, data_format="channels_last", activation="relu"))
# model.add(Dense(input_layer_neurons=16, hidden_layer_neurons=32, kernel_initializer='normal', activation='relu'))
# model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
model.add(BatchNormalization())
model.add(Dense(units=64, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(units=16, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(units=3, activation='softmax'))  # units = nums of classes

# training
his = LossHistory()
model.compile(loss='categorical_crossentropy', optimizer=Adam(0.0001), metrics=['accuracy'])
model.fit(X_train, Y_train, batch_size=32, epochs=20, verbose=1, validation_data=(X_test, Y_test), callbacks=[his])
model.summary()
his.loss_plot('epoch')
model.save('C:\\Users\\min\\Desktop\\project\\A-free\\Action\\a-free-1.h5')

# evaluate and draw confusion matrix
print('Test:')
score, accuracy = model.evaluate(X_test,Y_test,batch_size=32)
print('Test Score:{:.3}'.format(score))
print('Test accuracy:{:.3}'.format(accuracy))
# confusion matrix
Y_pred = model.predict(X_test)
cfm = confusion_matrix(np.argmax(Y_test,axis=1), np.argmax(Y_pred, axis=1))
np.set_printoptions(precision=2)

plt.figure()
class_names = ['stand:0','m_kick:1','h_kick:2']#,'h_paul','l_paul']
plot_confusion_matrix(cfm, classes=class_names, title='Confusion Matrix')
plt.show()

    
# test
model = load_model('a-free-1.h5')

test_input = [0.43, 0.46, 0.43, 0.52, 0.4, 0.52, 0.39, 0.61, 0.4,
              0.67, 0.46, 0.52, 0.46, 0.61, 0.46, 0.67, 0.42, 0.67,
              0.42, 0.81, 0.43, 0.91, 0.45, 0.67, 0.45, 0.81, 0.45,
              0.91, 0.42, 0.44, 0.43, 0.44, 0.42, 0.46, 0.44, 0.46]
test_np = np.array(test_input)
test_np = test_np.reshape(-1, 36)

# test_np = np.array(X[1033]).reshape(-1, 36)
if test_np.size > 0:
    pred = np.argmax(model.predict(test_np))
    init_label = Actions(pred).name
    print(init_label)
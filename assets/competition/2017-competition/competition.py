import pandas as pd
import numpy as np
# For split train set
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, Input, Embedding, LSTM, Masking
from keras.layers.wrappers import TimeDistributed
from keras.layers.recurrent import GRU
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.merge import Add
from keras.regularizers import l2
from keras.layers.normalization import BatchNormalization
from keras import backend as K
import tensorflow as tf
from sklearn.model_selection import KFold
from keras.callbacks import Callback , ModelCheckpoint, EarlyStopping
from keras.models import model_from_json 
import sys
from keras.utils import plot_model
import os
from datetime import datetime 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#%matplotlib inline
now = datetime.now()
nowDatetime = now.strftime('%Y-%m-%d_%H:%M')
np.random.seed(777)
# Print all Numpy Array
np.set_printoptions(threshold=np.nan)
res_ff = open("result_test_noncv","a")
dir_tmp = ["./best_weight","./cv_label","./final_label"]
for i in dir_tmp :
    if not os.path.exists(i ):
        os.mkdir (i )


# Define Class Earlystopping by validtaion loss
class EarlyStoppingByLossVal(Callback):
    def __init__(self, monitor='val_loss', value=0.00001, verbose=0):
        super(Callback, self).__init__()
        self.monitor = monitor
        self.value = value
        self.verbose = verbose

    def on_epoch_end(self, epoch, logs={}):
        current = logs.get(self.monitor)
        if current is None:
            warnings.warn("Early stopping requires %s available!" % self.monitor, RuntimeWarning)

        if current < self.value:
            if self.verbose > 0:
                res_f.write("Epoch %05d: early stopping THR\n" % epoch)
            self.model.stop_training = True

# Define Custom Metric
def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def f1(y_true, y_pred):
    def precision(y_true, y_pred):
       true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
       predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
       precision = true_positives / (predicted_positives + K.epsilon())
       return precision
    def recall(y_true, y_pred):
       true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
       possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
       recall = true_positives / (possible_positives + K.epsilon())
       return recall

    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall))

# Get Data Description 
#   train_id,test1_id,test2_id : Account ID
#   X : Train Overall Data, Y : Train Label Data, Z : Train Daily Data
#   X1, Y1 ,Z1 : Test1 Data
#   X2, Y2 ,Z2 : Test2 Data
#traindata = np.load("./bns_churn_data_norm_mask.npz")
traindata = np.load("./bns_churn_data_norm.npz")

# Check Data Shape
print( np.shape(traindata['X']))
print (np.shape(traindata['Y']))
print (np.shape(traindata['Z']))

# Split Train Set 
#X_train, X_test1, y_train, y_test1,Z_train,Z_test1,X_label,X_label1 = train_test_split(traindata['X1'], traindata['Y1'],traindata['Z1'],traindata["train_id"], test_size=0.33, random_state=42)

y_train = traindata["Y"]
y_test1 = traindata["Y1"]
y_test2 = traindata["Y2"]

X_train = traindata["X"].reshape(3999,1106)
X_test1 = traindata["X1"].reshape(3000,1106)
X_test2 = traindata["X2"].reshape(3000,1106)

Z_train = traindata["Z"]
Z_test1 = traindata["Z1"]
Z_test2 = traindata["Z2"]

# Get AccuontID from Numpy
X_label = traindata["train_id"]
X_label1 = traindata["test1_id"]
X_label2 = traindata["test2_id"]

# Remove Date Column 
#Z_train = Z_train[:, :, 1:122]
#Z_test1 = Z_test1[:, :, 1:122]
#Z_test2 = Z_test2[:, :, 1:122]


# Reshape Numpy Array 
X_train = X_train.astype('float32')
X_test1 = X_test1.astype('float32')
X_test2 = X_test1.astype('float32')

X_train = np.concatenate((X_train, X_test1), axis=0)
y_train = np.concatenate((y_train, y_test1), axis=0)
Z_train = np.concatenate((Z_train, Z_test1), axis=0)
X_label = np.concatenate((X_label, X_label1), axis=0)


X_train = np.concatenate((X_train, X_test2), axis=0)
y_train = np.concatenate((y_train, y_test2), axis=0)
Z_train = np.concatenate((Z_train, Z_test2), axis=0)
X_label = np.concatenate((X_label, X_label2), axis=0)

# Define Callback
callbacks = [
    EarlyStopping(monitor='val_f1', min_delta=0.01, patience=15, verbose=1, mode='max')	
    #EarlyStoppingByLossVal(monitor='val_loss', value=0.00001, verbose=1),
    #ModelCheckpoint(filepath='./best_weight/kfold_weights'+nowDatetime+'.hdf5', monitor='val_loss', save_best_only=True, verbose=0),
]

fold_cnt = 1

# Define Prams
epochs = 20
batch_size = 40
l2_lambda = 0.0001
drop_out = [0.5, 0.4, 0.4, 0.5, 0.4, 0.25]
RNN_dense = [142, 64]
DNN_dense = [800, 500, 400]
gru = [142, 64]


# Loop for resize Epochs and Batch
res_ff.write(nowDatetime+" Prams \n"+"  Epochs : "+str(epochs)+"\n  Batch_size : "+str(batch_size)+"\n  Drop_out : "+str(drop_out)+"\n  RNN_dense : " +str(RNN_dense)+"\n  DNN_dense : " +str(DNN_dense)+"\n  GRU : "+str(gru) +"\n")
# RNN Model
main_input = Input(shape=np.shape(Z_train[1]), dtype='float32', name='main_input') # Shape (None,41,123)
main_inp = BatchNormalization()(main_input)
x = Masking(mask_value=0.)(main_inp)
x = Dropout(float(drop_out[0]))(x)
x = TimeDistributed(Dense(int(RNN_dense[0]), kernel_initializer='normal'))(x) # Shape (None,41,256)
x = LeakyReLU()(x)
x = GRU(units=int(gru[0]), return_sequences=True)(x)
x = Dropout(float(drop_out[1]))(x)
# ManyToMany 
#x = GRU(64, return_sequences=True)(x)# Shape (None,41,64)
#x = Flatten()(x # Shape (None,41*64))
# ManyToOne
x = TimeDistributed(Dense(int(RNN_dense[1]), kernel_initializer='glorot_uniform', activation='sigmoid'))(x)# Shape (None,41,64)
x = GRU(int(gru[1]), return_sequences=False)(x)# Shape (None,64)a

# DNN Model
sub_input = Input(shape=np.shape(X_train[1]), dtype='float32', name='sub_input')# Shape (None,1,1097)
sub_inp = BatchNormalization()(sub_input)
y = Dropout(float(drop_out[2]))(sub_inp)
y = Dense(int(DNN_dense[0]), kernel_initializer='he_uniform', activation='relu')(y)# Shape (None,1,2048)
#y = LeakyReLU()(y)
y = Dropout(float(drop_out[3]))(y)
y = Dense(int(DNN_dense[1]), kernel_initializer='he_uniform', kernel_regularizer=l2(l2_lambda), activation='relu')(y)# Shape (None,1,2048)

# Merge Model ( Concat )
x = keras.layers.concatenate([x, y])# Shape (None,2048+64)
x = Dropout(float(drop_out[4]))(x)
x = BatchNormalization()(x)
x = Dense(int(DNN_dense[2]), kernel_initializer='he_uniform', activation='relu')(x)# Shape (None,256)
x = Dropout(float(drop_out[5]))(x)
main_output = Dense(1, activation='sigmoid', kernel_initializer='glorot_uniform', kernel_regularizer=l2(l2_lambda),name='main_output')(x)# Shape (None,1)
model = Model(inputs=[main_input, sub_input], outputs=main_output)

# Set Optimizer
opt = keras.optimizers.Adam(lr=0.0005)
# Set Complie Method
model.compile(optimizer=opt,
              loss={'main_output': 'binary_crossentropy'},
              metrics=['binary_accuracy',f1,recall,precision])
#print (model.summary())
#plot_model(model, to_file='multilayer_perceptron_graph.png')
# Train Model with Validation Data
history = model.fit({'main_input': Z_train, 'sub_input': X_train},
          {'main_output': y_train},
           epochs=int(epochs), batch_size=int(batch_size),
	   validation_split=0.3)
           #validation_data=([Z_test1,X_test1], y_test1),	   
           #callbacks=callbacks)
# Save Model
model_json = model.to_json()
with open("./best_weight/model_norm.json", "w") as json_file : 
   json_file.write(model_json)

history_dict = history.history
history_dict.keys()

loss_values = history_dict['loss'][3:]
val_loss_values = history_dict['val_loss'][3:]
epochs = range(1, len(loss_values) + 1)

plt.plot(epochs, loss_values, 'bo')
plt.plot(epochs, val_loss_values, 'b+')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.savefig('res.png')


# Get Score Test1, Test2
score_1 = model.evaluate([Z_test1,X_test1], y_test1, verbose = 1)
score_2 = model.evaluate([Z_test2,X_test2], y_test2, verbose = 1)


res_ff.write("Test1\n  [Loss, Accuracy, Fscore, Recall, Precision]\n  "+str(score_1)+"\n")
res_ff.write("Test2\n  [Loss, Accuracy, Fscore, Recall, Precision]\n  "+str(score_2)+"\n")
#Predict label
res1 = model.predict([Z_test1,X_test1])
res2 = model.predict([Z_test2,X_test2])

f = open("./cv_label/res_label_test1_"+nowDatetime , "w")
ii = 0
for i in res1 :
   f.write(str(X_label1[ii]).replace("b'",'').replace("'",'')+","+str(i.round(2)).replace("]",'').replace("[ ",'')+"\n")
   ii = ii+1
f.close()
ii= 0
f = open("./cv_label/res_label_test2_"+nowDatetime , "w")
for i in res2 :
   f.write(str(X_label2[ii]).replace("b'",'').replace("'",'')+","+str(i.round(2)).replace("]",'').replace("[ ",'')+"\n")
   ii = ii+1
f.close()

# Clear Model
K.clear_session()
del model
del x
del y
del main_input
del sub_input

#res_f.write("------------------------------------------------------------------------------------------------------\n\n")      


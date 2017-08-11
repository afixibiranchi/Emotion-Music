import model_emotion
import settings_emotion
import tensorflow as tf
import numpy as np
import time
import os
from sklearn import metrics
from scipy import misc
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

dataset = pd.read_csv('fer2013.csv')
data_train = dataset.loc[dataset['Usage'] == 'Training'].values.copy()[:5000, :]
data_test = dataset.loc[dataset['Usage'] == 'PublicTest'].values.copy()[:100, :]

sess = tf.InteractiveSession()
model = model_emotion.Model(len(settings_emotion.label))
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver(tf.global_variables())

try:
    saver.restore(sess, os.getcwd() + "/model.ckpt")
    print 'load model..'
except:
    print 'start from fresh variables'

LOST, ACC_TRAIN, ACC_TEST = [], [], []
for i in xrange(settings_emotion.epoch):
    total_cost, total_accuracy, last_time = 0, 0, time.time()
    for k in xrange(0, (data_train.shape[0] // settings_emotion.batch_size) * settings_emotion.batch_size, settings_emotion.batch_size):
        emb_data = np.zeros((settings_emotion.batch_size, settings_emotion.image_size, settings_emotion.image_size, 1), dtype = np.float32)
        emb_data_label = np.zeros((settings_emotion.batch_size, len(settings_emotion.label)), dtype = np.float32)
        
        for x in xrange(settings_emotion.batch_size):
            image = data_train[k + x, 1].split(' ')
            image = np.array([int(m) for m in image])
            emb_data_label[x, int(data_train[k + x, 0])] = 1.0
            emb_data[x, :, :, :] = image.reshape((settings_emotion.image_size, settings_emotion.image_size, 1)) / 255.0
            
        _, loss = sess.run([model.optimizer, model.cost], feed_dict = {model.X : emb_data, model.Y : emb_data_label, 
                                                                       model.learning_rate: settings_emotion.learning_rate})
        accuracy = sess.run(model.accuracy, feed_dict = {model.X : emb_data, model.Y : emb_data_label, 
                                                         model.learning_rate: settings_emotion.learning_rate})
        total_cost += loss
        total_accuracy += accuracy
        
    total_cost /= (data_train.shape[0] // settings_emotion.batch_size)
    LOST.append(total_cost)
    total_accuracy /= (data_train.shape[0] // settings_emotion.batch_size)
    ACC_TRAIN.append(total_accuracy)
    print "epoch: " + str(i + 1) + ", loss: " + str(loss) + ", accuracy: " + str(total_accuracy) + ", s / epoch: " + str(time.time() - last_time)
    
    total_accuracy, total_logits, total_true = 0, [], []
    for k in xrange(0, (data_test.shape[0] // settings_emotion.batch_size) * settings_emotion.batch_size, settings_emotion.batch_size):
        emb_data = np.zeros((settings_emotion.batch_size, settings_emotion.image_size, settings_emotion.image_size, 1), dtype = np.float32)
        emb_data_label = np.zeros((settings_emotion.batch_size, len(settings_emotion.label)), dtype = np.float32)
        
        for x in xrange(settings_emotion.batch_size):
            image = data_test[k + x, 1].split(' ')
            image = np.array([int(m) for m in image])
            emb_data_label[x, int(data_test[k + x, 0])] = 1.0
            total_true.append(int(data_test[k + x, 0]))
            emb_data[x, :, :, :] = image.reshape((settings_emotion.image_size, settings_emotion.image_size, 1)) / 255.0
            
        accuracy, logits = sess.run([model.accuracy, tf.cast(tf.argmax(model.logits, 1), tf.int32)], feed_dict = {model.X : emb_data, model.Y : emb_data_label})
        total_accuracy += accuracy
        total_logits += logits.tolist()
    
    total_accuracy /= (data_test.shape[0] // settings_emotion.batch_size)
    ACC_TEST.append(total_accuracy)
    print 'testing accuracy: ' + str(total_accuracy)
    print(metrics.classification_report(total_true, np.array(total_logits), target_names = settings_emotion.label))
    
saver.save(sess, os.getcwd() + '/model.ckpt')
plt.figure(figsize = (20, 10))
xtick = [i for i in xrange(len(LOST))]
plt.subplot(1, 2, 1)
plt.plot(xtick, LOST)
plt.subplot(1, 2, 2)
plt.plot(xtick, ACC_TRAIN, label = 'acc train')
plt.plot(xtick, ACC_TEST, label = 'acc test')
plt.legend()
plt.savefig('plot.png')
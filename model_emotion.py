import tensorflow as tf
import numpy as np
import settings_emotion

class Model:
	
	def __init__(self, output_shape):
		
		# image must size 90, 90, 1
		self.X = tf.placeholder('float', [None, settings_emotion.picture_dimension, settings_emotion.picture_dimension, 1])
		self.Y = tf.placeholder('float', [None, output_shape])
		
		def conv_layer(x, conv, out_shape, name, stride = 1):
			w = tf.Variable(tf.truncated_normal([conv, conv, int(x.shape[3]), out_shape]), name = name + '_w')
			b = tf.Variable(tf.truncated_normal([out_shape], stddev = 0.01), name = name + '_b')
			return tf.nn.conv2d(x, w, [1, stride, stride, 1], padding = 'SAME') + b
		
		def fully_connected(x, out_shape, name):
			w = tf.Variable(tf.truncated_normal([int(x.shape[1]), out_shape]), name = name + '_fc_w')
			b = tf.Variable(tf.truncated_normal([out_shape], stddev = 0.01), name = name + '_fc_b')
			return tf.matmul(x, w) + b
		
		def pooling(x, k = 2, stride = 2):
			return tf.nn.max_pool(x, ksize = [1, k, k, 1], strides = [1, stride, stride, 1], padding = 'SAME')
		
		with tf.name_scope("conv3-8-1"):
			conv1 = tf.nn.relu(conv_layer(self.X, 3, 8, '8-1'))
			
		with tf.name_scope("maxpool-1"):
			pooling1 = pooling(conv1, stride = 2)
		
		with tf.name_scope("conv3-16-1"):
			conv2 = tf.nn.relu(conv_layer(pooling1, 3, 16, '16-1'))
			
		with tf.name_scope("conv3-16-2"):
			conv3 = tf.nn.relu(conv_layer(conv2, 3, 16, '16-2'))
			
		with tf.name_scope("maxpool-2"):
			pooling2 = pooling(conv3, stride = 2)
			
		with tf.name_scope("conv3-32-1"):
			conv4 = tf.nn.relu(conv_layer(pooling2, 3, 32, '128-1'))
			
		with tf.name_scope("conv3-32-2"):
			conv5 = tf.nn.relu(conv_layer(conv4, 3, 32, '128-2'))
			
		with tf.name_scope("maxpool-3"):
			pooling3 = pooling(conv5, stride = 2)
			
		with tf.name_scope("conv3-64-1"):
			conv6 = tf.nn.sigmoid(conv_layer(pooling3, 3, 64, '64-1'))
			
		with tf.name_scope("maxpool-4"):
			pooling4 = pooling(conv6, stride = 2)
			
		with tf.name_scope("fc-1024-1"):
			pooling4 = tf.reshape(pooling4, [-1, 6 * 6 * 64])
			fc1 = tf.nn.sigmoid(fully_connected(pooling4, 1024, '512_1'))
			
		with tf.name_scope("fc-512-1"):
			fc2 = tf.nn.sigmoid(fully_connected(fc1, 512, '128_1'))
		
		with tf.name_scope("fc-128-1"):
			fc3 = tf.nn.sigmoid(fully_connected(fc2, 128, '128_1'))
			
		with tf.name_scope("logits"):
			self.logits = fully_connected(fc3, output_shape, 'logits')
			
		self.outputs = tf.nn.softmax(self.logits)
		
		self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels = self.Y, logits = self.logits))
		self.optimizer = tf.train.AdamOptimizer(settings_emotion.learning_rate).minimize(self.cost)
		
		correct_prediction = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self.Y, 1))
		self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
'''		
g = tf.Graph()

with g.as_default():
	model = Model(3)
	
tf.summary.FileWriter("logs", g).close()
'''
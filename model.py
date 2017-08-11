import tensorflow as tf
import numpy as np

class Model:
	
	def __init__(self, images, output_shape):
		
		# image must size 114, 114, 3, RGB
		self.X = tf.placeholder('float', [None, images.shape[1], images.shape[2], images.shape[3]])
		self.Y = tf.placeholder('float', [None, output_shape])
		self.learning_rate = tf.placeholder('float')
		
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
		
		with tf.name_scope("conv3-32-1"):
			conv1 = tf.nn.relu(conv_layer(self.X, 3, 32, '32-1'))
			
		with tf.name_scope("maxpool-1"):
			pooling1 = pooling(conv1, stride = 2)
		
		with tf.name_scope("conv3-64-1"):
			conv2 = tf.nn.relu(conv_layer(pooling1, 3, 64, '64-1'))
			
		with tf.name_scope("conv3-64-2"):
			conv3 = tf.nn.relu(conv_layer(conv2, 3, 64, '64-2'))
			
		with tf.name_scope("maxpool-2"):
			pooling2 = pooling(conv3, stride = 2)
			
		with tf.name_scope("conv3-128-1"):
			conv3 = tf.nn.relu(conv_layer(pooling2, 3, 128, '128-1'))
			
		with tf.name_scope("conv3-128-2"):
			conv4 = tf.nn.relu(conv_layer(conv3, 3, 128, '128-2'))
			
		with tf.name_scope("maxpool-3"):
			pooling3 = pooling(conv4, stride = 2)
			
		with tf.name_scope("conv3-128-3"):
			conv5 = tf.nn.relu(conv_layer(pooling3, 3, 128, '128-3'))
			
		with tf.name_scope("maxpool-4"):
			pooling4 = pooling(conv5, stride = 2)
			
		with tf.name_scope("fc-4096-1"):
			pooling4 = tf.reshape(pooling4, [-1, 8 * 8 * 128])
			fc1 = tf.nn.tanh(fully_connected(pooling4, 4096, '4096_1'))
		
		with tf.name_scope("fc-4096-2"):
			fc2 = tf.nn.tanh(fully_connected(fc1, 4096, '4096_2'))
			
		with tf.name_scope("fc-1000"):
			fc3 = tf.nn.tanh(fully_connected(fc2, 1000, '1000'))
			
		with tf.name_scope("logits"):
			self.logits = fully_connected(fc3, output_shape, 'logits')
			
		self.outputs = tf.nn.softmax(self.logits)
		
		self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels = self.Y, logits = self.logits))
		self.optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(self.cost)
		
		correct_prediction = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self.Y, 1))
		self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
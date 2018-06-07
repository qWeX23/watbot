import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import datasets
from sklearn.cross_validation import train_test_split

def iter_data(x,y,batch_size):
    for start_index in range(0,len(x),batch_size):
        end_index = start_index+batch_size
        yield x[start_index:end_index],y[start_index:end_index]

def get_learning(i,total,lr):
    progress =  i/total
    lr = lr * (1 - progress)
    return lr


#make Tensors
X = tf.placeholder(tf.float32,[None,27,48,3]) #Data
Y = tf.placeholder(tf.float32,[None,2]) #Labels

w = tf.get_variable("w",[5,5,3,32],initializer = tf.random_normal_initializer(stddev=0.01))
w2  = tf.get_variable("w2",[5,5,32,64],initializer = tf.random_normal_initializer(stddev=0.01))
w3  = tf.get_variable("w3",[5,5,64,128],initializer = tf.random_normal_initializer(stddev=0.01))
w_clf = tf.get_variable("w_clf",[128,2],initializer=tf.random_normal_initializer(stddev=0.01))

h = tf.nn.conv2d(X,w,[1,1,1,1],"SAME")
h = tf.nn.relu(h)
print("H_pre",h.get_shape())
h = tf.nn.max_pool(h,[1,2,2,1],[1,2,2,1],"VALID")
print("H",h.get_shape())


h2 = tf.nn.conv2d(h,w2,[1,1,1,1],"SAME")
print("H2_pre",h2.get_shape())
h2 = tf.nn.relu(h2)
h2 = tf.nn.max_pool(h2,[1,2,2,1],[1,2,2,1],"VALID")
print("H2_post",h2.get_shape())


h3 = tf.nn.conv2d(h2,w3,[1,1,1,1],"SAME")
print("H3_pre",h3.get_shape())
h3 = tf.nn.relu(h3)
h3 = tf.reduce_mean(h3,axis=[1,2])
print("H3_post",h3.get_shape())

logits = tf.matmul(h3,w_clf)

loss = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y)
loss = tf.reduce_mean(loss)

learning_rate = tf.placeholder(tf.float32,[],name="learning_rate")
train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

prediction = tf.argmax(logits, 1)
correct = tf.equal(prediction, tf.argmax(Y, 1))
acc = tf.reduce_mean(tf.cast(correct, tf.float32))*100

num_iter = 100
num_batches = 500
num_batch = 10
labels_matrix = np.eye(2)
batch_size = 64
base_lr = 0.004
current_lr = base_lr

x_data,y_data = datasets.das_v2("../../data")
x_data = x_data / 255
train_X, test_X, train_Y, test_Y = train_test_split(x_data, y_data, test_size=0.2, random_state=42)


with tf.Session() as sess:
    tf.initialize_all_variables().run()
    for iteration in range(num_iter):
        current_lr = get_learning(iteration,num_iter,base_lr)
        for x_batch,y_batch in iter_data(train_X,train_Y,batch_size):
            y_batch = labels_matrix[y_batch]
            train_result, nploss = sess.run([train,loss],{X:x_batch,Y:y_batch,learning_rate:current_lr})
        score = sess.run(acc,{X:test_X,Y:labels_matrix[test_Y]})
        score_train = sess.run(acc,{X:train_X[:len(test_X)],Y:labels_matrix[train_Y[:len(test_Y)]]})
        print("I: %d TEST: %.2f TRAIN: %.2f"%(iteration,score,score_train))

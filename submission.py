import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import os

BATCH_SIZE = 32
EPOCHS = 10

(x_train_full, y_train_full), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()

x_train_full = x_train_full / 255.0
x_test = x_test / 255.0 

x_train_full = np.expand_dims(x_train_full, -1)
x_test = np.expand_dims(x_test, -1)

# Total samples = 60,000
val_size = 12000

x_val = x_train_full[-val_size:]
y_val = y_train_full[-val_size:]

x_train = x_train_full[:-val_size] # First 48,000
y_train = y_train_full[:-val_size]

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

model = keras.Sequential([
    # Input shape is (28, 28, 1)
    layers.Conv2D(filters=28, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(filters=56, kernel_size=(3, 3), activation='relu'),

    layers.Flatten(),

    layers.Dense(units=56, activation='relu'),
    layers.Dense(units=10, activation='softmax') # 10 classes
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


model.summary()


history = model.fit(x_train, y_train,
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    validation_data=(x_val, y_val))

plt.figure(figsize=(10, 6))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy vs. Epoch')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')


if not os.path.exists('imgs'):
    os.makedirs('imgs')

plt.savefig('imgs/accuracy_plot.png')


test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"\nTest Accuracy: {test_acc:.4f}")

y_pred_probs = model.predict(x_test)
y_pred_labels = np.argmax(y_pred_probs, axis=1)


for target_class in range(10):
    found = False
    for i in range(len(x_test)):
        if y_test[i] == target_class and y_pred_labels[i] != target_class:
            # Found one
            img = x_test[i].reshape(28, 28) # Reshape back to 2D for plotting
            true_label = class_names[y_test[i]]
            pred_label = class_names[y_pred_labels[i]]

            plt.figure()
            plt.imshow(img, cmap='gray')
            plt.title(f"True: {true_label} (Class {target_class})\nPred: {pred_label}")
            plt.axis('off')

            filename = f'imgs/misclassified_example_{target_class}.png'
            plt.savefig(filename)

            found = True
            break # Move to the next class
    if not found:
        print(f"No misclassified examples found for class {target_class} ({class_names[target_class]})")


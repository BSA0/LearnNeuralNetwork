from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense
from keras.models import load_model
from keras.utils import plot_model
import os
import json
import cv2 as cv

# Каталог с данными для обучения
train_dir = r"E:\CropNums\ForNeural\train"
# Каталог с данными для проверки
val_dir = r"E:\CropNums\ForNeural\val"
# Каталог с данными для тестирования
test_dir = r"E:\CropNums\ForNeural\test"
# Размеры изображения
img_width, img_height = 104, 23
# Размерность тензора на основе изображения для входных данных в нейронную сеть
# backend Tensorflow, channels_last
input_shape = (img_width, img_height, 3)
# Количество эпох
epochs = 30
# Размер мини-выборки
batch_size = 16
# Количество изображений для обучения
nb_train_samples = 98
# Количество изображений для проверки
nb_validation_samples = 21
# Количество изображений для тестирования
nb_test_samples = 21

if os.path.exists(r"E:\CropNums\my_model.h5"):
    model = load_model(r"E:\CropNums\my_model.h5")

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
else:
    model = Sequential()
    model.add(Conv2D(64, (3, 3), input_shape=input_shape))  # , activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())

    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

val_generator = datagen.flow_from_directory(
    val_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

test_generator = datagen.flow_from_directory(
    test_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=val_generator,
    validation_steps=nb_validation_samples // batch_size)

scores = model.evaluate_generator(test_generator, nb_test_samples // batch_size)
print(scores)
print("Аккуратность на тестовых данных: %.2f%%" % (scores[1]*100))

model.summary()
model.save(r"E:\CropNums\my_model.h5")
plot_model(model, to_file=r'C:\Users\belok\PycharmProjects\LearnNeuralNetwork\model.png')

img_arr = cv.imread("num2.bmp", 1)
# new_arr = cv.resize(img_arr, (104, 23))
# new_arr = new_arr.reshape(104, 23, 3)
cv.imshow("1", img_arr)
cv.waitKey(0)
cv.destroyAllWindows()
img_arr = img_arr.reshape(-1, 104, 23, 3)

print(model.predict(img_arr))

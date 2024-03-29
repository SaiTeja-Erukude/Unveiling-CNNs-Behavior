# VGG16 Architecture from scratch

# Importing libraries
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D , Flatten
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping


# Define your data directories and other parameters
train_data_dir = '../../data/imagenette2-320/train/'
val_data_dir = '../../data/imagenette2-320/val/'
img_height, img_width = 224, 224
epochs = 100

# Create trainb data generators
train_data_gen = ImageDataGenerator(rescale=1./255)
train_data = train_data_gen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width)
)

# Create validation data generator
val_data_gen = ImageDataGenerator(rescale=1./255)
val_data = val_data_gen.flow_from_directory(
    val_data_dir,
    target_size=(img_height, img_width)
)

# Instantiation
model = Sequential()

model.add(Conv2D(input_shape=(224,224,3), filters=64, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=64, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))

model.add(Flatten())
model.add(Dense(4096, activation="relu"))
model.add(Dense(4096, activation="relu"))
model.add(Dense(10, activation="softmax"))

model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

checkpoint = ModelCheckpoint(
    "vgg16_adam.h5",
    monitor='val_accuracy',
    save_best_only=True,
    save_weights_only=False,
    mode='max',
    period=1
)

early = EarlyStopping(
    monitor='val_accuracy',
    patience=20,
    verbose=1,
    mode='max'
)

hist = model.fit_generator(
    steps_per_epoch=100,
    generator=train_data,
    validation_data=val_data,
    validation_steps=10,
    epochs=epochs,
    verbose=1,
    callbacks=[checkpoint, early]
)
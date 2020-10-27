from model import data, model
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.models import load_model


save_path = Path("model.h5")


if __name__ == '__main__':
    train, val = data()
    if not save_path.exists():
        model = model()
        model.compile("adam", "categorical_crossentropy", metrics=["acc"])
        initial_epoch = 1
    else:
        model = load_model(save_path)
        initial_epoch = 101
    checkpoint = tf.keras.callbacks.ModelCheckpoint(save_path, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    model.fit(train, validation_data=val, epochs=200, callbacks=[checkpoint], initial_epoch=initial_epoch)

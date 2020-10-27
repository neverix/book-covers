from train import save_path
from tensorflow.keras.models import load_model
from gen import Document
import numpy as np


batch_size = 1024
batches = 50


if __name__ == '__main__':
    out = open("out.png", 'wb')
    doc = Document("This is a Test Book")
    model = load_model(save_path)
    for i in range(1, batches + 1):
        rate = max(0.05, 1 / i)
        imgs = []
        docs = []
        for _ in range(batch_size):
            new_doc = doc.mutate(rate)
            img = np.array(new_doc.draw())
            imgs.append(img)
            docs.append(new_doc)
        inputs = np.stack(imgs, 0)
        predictions = model.predict(inputs)
        predictions *= np.linspace(0, 10, 10)
        predictions = np.max(predictions, axis=-1)
        best = int(np.quantile(predictions, 0.9))
        doc = docs[best]
        doc.draw().save(out)
        out.flush()
        print(i)

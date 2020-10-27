import tensorflow as tf
import shutil
from pathlib import Path
import pandas as pd


def model():
    return tf.keras.applications.MobileNetV2(input_shape=(256, 256, 3), classes=10, weights=None)


def data(csv_path="main_dataset.csv", out_path=Path("out")):
    print(tf.__version__)
    if not out_path.exists():
        df = pd.read_csv(csv_path)
        df.stars = pd.Categorical(df.book_depository_stars).codes
        for star, df in df.groupby(df.stars):
            out_dir = out_path / str(star)
            out_dir.mkdir(parents=True, exist_ok=True)
            for img_path in df.img_paths:
                img_path = Path(img_path)
                out_img_path = out_dir / f"{img_path.parent.stem}_{img_path.stem}{img_path.suffix}"
                shutil.copy(img_path, out_img_path)
    ds = tf.keras.preprocessing.image_dataset_from_directory(out_path)
    ds = ds.map(lambda x, y: (x, tf.one_hot(y, depth=10)))
    val_size = len(ds) // 10
    return ds.skip(val_size), ds.take(val_size)

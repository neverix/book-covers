from doc import Doc, Proxy, randint, choice, tuproxy
from pathlib import Path
from image_utils import ImageText


class Document(Doc):
    def __init__(self, title):
        self.title = title

        self.rgb = tuproxy(3, 128, randint(256))

        self.fonts = list(Path("fonts").iterdir())
        self.font = Proxy(0, choice(len(self.fonts)))
        self.text_pos = tuproxy(2, 128, randint(256))
        self.text_width = Proxy(128, randint(256))
        self.text_rgb = tuproxy(3, 128, randint(256))
        self.text_size = Proxy(3, randint(50, 10))

        self.grad_x = Proxy(128, randint(256, -256))
        self.grad_x_rgb = tuproxy(3, 128, randint(256))

        self.grad_y = Proxy(128, randint(256, -256))
        self.grad_y_rgb = tuproxy(3, 128, randint(256))

    def draw(self):
        img = ImageText((256, 256), background=self.rgb.v)
        img.draw.rectangle((-1, -1, self.grad_x.v, 256), fill=self.grad_x_rgb.v)
        img.draw.rectangle((-1, -1, 256, self.grad_y.v), fill=self.grad_y_rgb.v)
        font = str(self.fonts[self.font.v])
        img.write_text_box(self.text_pos.v, self.title, self.text_width.v,
                           font, self.text_size.v, self.text_rgb.v)
        return img.image


if __name__ == '__main__':
    doc = Document("This is a book title")
    doc = doc.mutate(1)
    doc.draw().save("out.png")

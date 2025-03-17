import cv2
import numpy as np
import skimage as sk
import torchvision.transforms as transforms

from PIL import Image
from typing import List, Tuple, Union
from skimage.filters import gaussian

from straug.weather import Fog, Snow, Frost, Rain, Shadow
from straug.noise import GaussianNoise, ShotNoise, SpeckleNoise
from straug.blur import GaussianBlur, DefocusBlur, MotionBlur, ZoomBlur


# Modified from the STR library to fix some errors
class ImpulseNoise:
    def __init__(self, rng=None):
        self.rng = np.random.default_rng() if rng is None else rng

    def __call__(self, img, mag=-1, prob=1.0):
        if self.rng.uniform(0, 1) > prob:
            return img

        b = [0.03, 0.07, 0.11]
        if mag < 0 or mag >= len(b):
            index = 0
        else:
            index = mag

        a = b[index]
        c = self.rng.uniform(a, a + 0.04)
        s = self.rng.integers(2**32, size=4)
        img = (
            sk.util.random_noise(np.asarray(img) / 255.0, mode="s&p", rng=s, amount=c)
            * 255
        )

        return Image.fromarray(img.astype(np.uint8))


# Modified from the STR library to fix some errors
class GlassBlur:
    def __init__(self, rng=None):
        self.rng = np.random.default_rng() if rng is None else rng

    def __call__(self, img, mag=-1, prob=1.0):
        if self.rng.uniform(0, 1) > prob:
            return img

        w, h = img.size
        c = [
            (0.45, 1, 1),
            (0.6, 1, 2),
            (0.75, 1, 2),
        ]
        if mag < 0 or mag >= len(c):
            index = self.rng.integers(0, len(c))
        else:
            index = mag

        c = c[index]

        img = np.uint8(gaussian(np.asarray(img) / 255.0, sigma=c[0]) * 255)

        # locally shuffle pixels
        for i in range(c[2]):
            for y in range(h - c[1], c[1], -1):
                for x in range(w - c[1], c[1], -1):
                    dx, dy = self.rng.integers(-c[1], c[1], size=(2,))
                    y_prime, x_prime = y + dy, x + dx
                    img[y, x], img[y_prime, x_prime] = img[y_prime, x_prime], img[y, x]

        img = np.clip(gaussian(img / 255.0, sigma=c[0]), 0, 1) * 255
        return Image.fromarray(img.astype(np.uint8))


class RandomSTRAugmentation:
    def __init__(
        self,
        mag_range: Tuple[int, int] = (-1, 3),
        prob_list: List[float] | int = 0.5,
    ):
        """
        STR-style augmentation combining blur/noise/weather effects

        Args:
            mag_range: Magnitude range for augmentations (min, max)
            prob_list: List of probabilities for each augmentation group
        """

        blur_aug = [GaussianBlur(), DefocusBlur(), MotionBlur(), GlassBlur(), ZoomBlur()]
        noise_aug = [GaussianNoise(), ShotNoise(), ImpulseNoise(), SpeckleNoise()]
        weather_aug = [Fog(), Snow(), Frost(), Rain(), Shadow()]

        self.aug_list = [blur_aug, noise_aug, weather_aug]
        self.mag_range = mag_range

        if isinstance(prob_list, (int, float)):
            self.prob_list = [prob_list] * len(self.aug_list)
        elif isinstance(prob_list, list):
            if len(prob_list) != len(self.aug_list):
                raise ValueError(f"prob_list must be of length {len(self.aug_list)}")
            self.prob_list = prob_list
        else:
            self.prob_list = [0.5] * len(self.aug_list)

    def __call__(self, img: Union[Image.Image, np.ndarray]):
        for i in range(len(self.aug_list)):
            if len(self.aug_list[i]) == 0:
                continue
            mag_range = np.random.randint(*self.mag_range)
            img = self.aug_list[i][np.random.randint(0, len(self.aug_list[i]))](
                img, mag=mag_range, prob=self.prob_list[i]
            )

        return img


if __name__ == "__main__":
    img_path = "./data/SoccerNet/test/images/0/0_1.jpg"

    transform = transforms.Compose([RandomSTRAugmentation()])
    image = Image.open(img_path).convert("RGB")
    augmented = transform(image)

    original = np.array(image)
    augmented = np.array(augmented)

    combined = np.hstack((original, augmented))
    combined_bgr = cv2.cvtColor(combined, cv2.COLOR_RGB2BGR)

    cv2.imwrite("random_strAug.jpg", combined_bgr)

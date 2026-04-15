import SimpleITK as sitk
import numpy as np

img = sitk.ReadImage(
    "/Users/wanghongyi/datasets/test_imaging/test_imaging/yang_xian_min_012Y/series10058-unknown/img0001-unknown.dcm"
)

arr = sitk.GetArrayFromImage(img)  # (1, H, W, 3)

rgb = arr[0]  # (H, W, 3)
print(rgb.shape, rgb.dtype)

import matplotlib.pyplot as plt

# plt.figure(figsize=(12,4))
# for i, c in enumerate(['R','G','B']):
#     plt.subplot(1,3,i+1)
#     plt.hist(rgb[:,:,i].ravel(), bins=256)
#     plt.title(c)
# plt.tight_layout()
# plt.show()

# diff = np.abs(rgb[:,:,0].astype(int) - rgb[:,:,1].astype(int)) + \
#        np.abs(rgb[:,:,1].astype(int) - rgb[:,:,2].astype(int))

# plt.imshow(diff, cmap='hot')
# plt.colorbar()
# plt.title("Color difference map")
# plt.show()

import cv2

rgb_uint8 = rgb.astype(np.uint8)
hsv = cv2.cvtColor(rgb_uint8, cv2.COLOR_RGB2HSV)

H, S, V = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]

plt.figure(figsize=(12,4))
plt.subplot(1,3,1); plt.imshow(H); plt.title("Hue")
plt.subplot(1,3,2); plt.imshow(S); plt.title("Saturation")
plt.subplot(1,3,3); plt.imshow(V); plt.title("Value")
plt.tight_layout()
plt.show()
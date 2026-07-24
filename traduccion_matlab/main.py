import numpy as np
import matplotlib.pyplot as plt
import cv2
import lbp_jmm
import sigma_jmm
import contract_jmm
import orbit_darts_jmm
import lbp_values_jmm
import imagen_jmm


# imagen_original = np.array([
#     [78, 99, 50],
#     [54, 54, 49],
#     [57, 12, 13]
# ])
# image = np.array([
#     [78, 99, 50, 70, 90, 55, 77, 66, 43],
#     [54, 54, 49, 77, 88, 81, 80, 72, 41],
#     [57, 12, 13, 52, 63, 54, 71, 32, 14]
# ])

image = np.array([
        [78, 99, 50],
        [54, 54, 49],
        [57, 12, 13]
    ])

s = 4

# image = cv2.imread('picaso.png')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# s = 134

darts_jll, darts_bypixel = lbp_jmm.lbp_jmm(image, s)
print(f"darts_jll queda:\n{darts_jll}")
print(f"darts_bypixel queda:\n{darts_bypixel}")
sigma_jmm = sigma_jmm.sigma_jll(darts_jll.copy(), darts_bypixel)
print(f"sigma_jmm queda:\n{sigma_jmm}")
darts_contract = contract_jmm.contract_jmm(sigma_jmm)
print(f"darts_contract queda:\n{darts_contract}")
orbit_darts = orbit_darts_jmm.orbit_darts_jmm(darts_contract)
print(f"orbit_darts_jmm queda:\n{orbit_darts}")
LBP_values = lbp_values_jmm.lbp_values_jmm(orbit_darts)
print(f"LBP_values queda:\n{LBP_values}")
LBP_img = imagen_jmm.imagen_jmm(darts_bypixel, LBP_values)
print(f"LBP_img queda:\n{LBP_img}")

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title('Imagen original')
plt.imshow(image)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('LBP Image')
plt.imshow(LBP_img)
plt.axis('off')

plt.show()

# save_img = cv2.cvtColor(LBP_img, cv2.COLOR_RGB2BGR)
# cv2.imwrite("Picaso_traduccion_final_ancho_134_imagen_jmm_original.png", save_img)

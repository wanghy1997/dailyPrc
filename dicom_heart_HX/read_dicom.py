

dicom = sitk.ReadImage(file_path)
data1 = np.squeeze(sitk.GetArrayFromImage(dicom))
data=data1+1024

center =50# ds.WindowCenter 50
width = 400#ds.WindowWidth # 400

win_min = (2 * center - width) / 2.0 + 0.5
win_max = (2 * center + width) / 2.0 + 0.5
dFactor = 255.0 / (win_max - win_min)
image = data1 - win_min #sitk读取的数值比pydicom读取的数值小1024

image1 = np.trunc(image * dFactor)#dFactor
image1[image1>255]=255
image1[image1<0]=0
image1=image1/255#np.uint8(image)
image1 = (image1 - 0.5)/0.5

image2=data#sitk读取的数值比pydicom读取的数值小1024
image2[image2<0]=0#-2000->0
image2=image2/4095
image2 = (image2 - 0.5)/0.5

# image1=(image1*2-1)*255
# image2=(image2*2-1)*255
# plt.subplot(2, 2, 1)
# plt.imshow(image1*255, cmap='gray')#,vmin=0,vmax=255
# plt.subplot(2, 2, 2)
# plt.imshow(image2*255, cmap='gray')#,vmin=0,vmax=255
# plt.show()

return image1,image2
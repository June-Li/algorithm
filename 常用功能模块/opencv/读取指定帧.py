import cv2

video_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_19/result.mp4'
cap = cv2.VideoCapture(video_path)
print('frame num: ', cap.get(7))
for i in range(340, int(cap.get(7))):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, image = cap.read()
    cv2.imshow('image', image)
    cv2.waitKey()

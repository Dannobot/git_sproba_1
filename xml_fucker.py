import numpy as np
import cv2
from lxml import etree
from io import StringIO, BytesIO
import os
import sys
from datetime import datetime
from datetime import timedelta
import json

def order_points(pts):
  # initialzie a list of coordinates that will be ordered
  # such that the first entry in the list is the top-left,
  # the second entry is the top-right, the third is the
  # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    rect[0] = pts[0]
    rect[1] = pts[1]
    rect[2] = pts[2]
    rect[3] = pts[3]
    return rect
  # the top-left point will have the smallest sum, whereas
  # the bottom-right point will have the largest sum
    x = 0
    iter = 0
    iterator = 0
    s = np.zeros((4, 1), dtype="int32")
    for i in np.nditer(pts.T.copy(order='C')):
        if iter == 0:
            x = i
            iter = iter + 1
        else:
            s[iterator] = (i + x)
    iterator = iterator + 1
    iter = 0
    # print("Sum:")
    # print(s)
    # print("Axis:")
    # print(np.argmin(s))
    # print(np.argmax(s))
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    x2 = 0
    y2 = 0
    max_x = 0
    max_y = 0
    iter2 = 0
    iter3 = 0
    # print("Lay:")
    for i2 in np.nditer(pts.T.copy(order='C')):
        if iter2 == 0:
            x2 = i2
        iter2 = iter2 + 1
    else:
        y2 = i2
    if max_x < x2:
        max_x = x2

    if max_y < y2:
        max_y = y2
    iter2 = 0
    iter3 = iter3 + 1
  # now, compute the difference between the points, the
  # top-right point will have the smallest difference,
  # whereas the bottom-left will have the largest difference
    x1 = 0
    iter1 = 0
    iterator1 = 0
    diff = np.zeros((4, 1), dtype="int32")
    for o in np.nditer(pts.T.copy(order='C')):
        if iter1 == 0:
            x1 = o
        iter1 = iter1 + 1
    else:
        diff[iterator1] = (o - x1)
        iterator1 = iterator1 + 1
        iter1 = 0
    # print("Diff:")
    # print(diff)
  # diff = np.diff(pts, axis=0)
    # print(np.argmin(diff))
    # print(np.argmax(diff))
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
  # return the ordered coordinates
    return rect

def four_point_transform(image, pts):
  # obtain a consistent order of the points and unpack them
  # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    # print(tl)
    # print(tr)
    # print(br)
    # print(bl)
  # compute the width of the new image, which will be the
  # maximum distance between bottom-right and bottom-left
  # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0])**2) + ((br[1] - bl[1])**2))
    widthB = np.sqrt(((tr[0] - tl[0])**2) + ((tr[1] - tl[1])**2))
    maxWidth = max(int(widthA), int(widthB))
  # compute the height of the new image, which will be the
  # maximum distance between the top-right and bottom-right
  # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(abs(((tr[0] - br[0])**2) + ((tr[1] - br[1])**2)))
    heightB = np.sqrt(abs(((tl[0] - bl[0])**2) + ((tl[1] - bl[1])**2)))
    if np.isnan(heightA):
        return

    maxHeight = max(int(heightA), int(heightB))
  # now that we have the dimensions of the new image, construct
  # the set of destination points to obtain a "birds eye view",
  # (i.e. top-down view) of the image, again specifying points
  # in the top-left, top-right, bottom-right, and bottom-left
  # order
    dst = np.array([
      [0, 0],
      [maxWidth - 1, 0],
      [maxWidth - 1, maxHeight - 1],
      [0, maxHeight - 1]], dtype="float32")
  # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
  # return the warped image
    return warped

def ananas():
  A_list = []
  xml = ''
  main_iter = 0
  main_iter_oc = 0
  main_iter_per_hour = 0
  main_iter_oc_per_hour = 0
  occupied = 0
  # if not os.path.exists('/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/'):
  #     os.makedirs('/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/')
  # if not os.path.exists('/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/Free/'):
  #     os.makedirs('/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/Free/')
  # if not os.path.exists('/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/Occupied/'):
  #     os.makedirs('/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/Occupied/')
  # file = open('/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/testfile.txt', 'w+')
  # fileoc = open('/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/Octestfile.txt', 'w+')
  diry = ""
  dir_old = ""
  prev_date = datetime.now()
  local_dir = os.path.dirname(os.path.realpath(__file__))
  for root, subdirs, files in os.walk(local_dir):
    # print(f'--root =  + {root}, {files}, {subdirs}')
    for filename in files:
      diry = root
      dir_old = diry
      file_path = os.path.join(root, filename)
  # print('\t- file %s (full path: %s)' % (filename, file_path))
      if "jpeg" in filename:
        # print(f'{filename}')
        img = cv2.imread(file_path, -1)
        data_big = cv2.imencode('.jpg', img)[1].tostring() # byte
        print(file_path)
        file_path = file_path[:-4]
        file_path += 'xml'
        filename = filename[:-4]
        filename += 'xml'
      #if "xml" in filename:
        # tree = etree.parse(file_path)
        print(file_path)
        # root = etree.fromstring()
        with open(file_path, 'r') as r:
          xml = r.read()
          # print(r.read())
        # print(etree.tostring('2013-02-26_15_09_35.xml', pretty_print=True))
        i = 0
        pts = np.empty([2, 0])
        for event, elem in etree.iterparse(file_path):
          if elem.tag == "space":
            if elem.get("occupied") is None:
              continue
            else:
              occupied = elem.get("occupied")
          if elem.tag == "point":
            i = i + 1
            tmo = np.array([int(elem.get('x')), int(elem.get('y'))])
            if i > 1:
              pts = np.concatenate((pts, tmo))
            else:
              pts = tmo
          if i == 4:
            pts = pts.reshape((-1, 1, 2))
            #print(pts)
            if pts.shape != (4, 1, 2):
              continue
            rect = cv2.boundingRect(pts)
            x, y, w, h = rect
            pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
            croped = img[y:y + h, x:x + w].copy()
            pts1 = pts - pts.min(axis=0)
            mask = np.zeros(croped.shape[:2], np.uint8)
            cv2.drawContours(mask, [pts1], -1, (255, 255, 255), -1, cv2.LINE_AA)
  ## (3) do bit-op
            dst = cv2.bitwise_and(croped, croped, mask=mask)
  # M = cv2.getPerspectiveTransform( pts.astype(np.float32),pts2)
  # dst = cv2.warpPerspective(img, M, (w, h))
            dst = four_point_transform(img, pts)
            # print(dst)
            if len(dst) == 0: #None:
              pts = np.empty([2, 0])
              i = 0
              continue
  # cv2.imshow("Image", warped)
            if occupied == "0":
              main_iter_per_hour = main_iter_per_hour + 1
              if main_iter_per_hour < 100:
                main_iter = main_iter + 1
                imgі = cv2.resize(dst, (64, 64))
                data = cv2.imencode('.jpg', imgі)[1].tostring() # byte
                A_list.append(str(data))
                # cv2.imwrite(f"/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/Free/{repr(main_iter)}.jpg", imgі)
            else:
              main_iter_oc_per_hour = main_iter_oc_per_hour + 1
              if main_iter_oc_per_hour < 100:
                main_iter_oc = main_iter_oc + 1
                imgі = cv2.resize(dst, (64, 64))
                data = cv2.imencode('.jpg', imgі)[1].tostring() # byte
                A_list.append(str(data))
                # with open(f"/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/Occupied/Oc{repr(main_iter_oc)}.jpg", "wb") as ee:
                #   ee.write(data)
                # cv2.imwrite(f"/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/Occupied/Oc{repr(main_iter_oc)}.jpg", imgі)
            
            # parsed_date = datetime.strptime(filename, "%Y-%m-%d_%H_%M_%S.xml")
            parsed_date = datetime.strptime(filename, "2013-02-26_15_09_35.xml")
            time_difference = prev_date - parsed_date
            time_difference_in_minutes = time_difference / timedelta(hours=1)
            if prev_date > parsed_date or time_difference_in_minutes >= 3:
              if main_iter_per_hour >= 100 and main_iter_oc_per_hour >= 100:
                main_iter_oc_per_hour = 0
            main_iter_per_hour = 0
            pts = np.empty([2, 0])
            i = 0
            continue
            prev_date = parsed_date
            if cv2.waitKey(33) == ord('a'):
              print("pressed a")
  # for child in elem:
  # if occupied == "1":
  # cv2.polylines(img, [pts], True, (0, 255, 255))
  # cv2.imshow("Image",img)
      i = 0
      continue
  ## (2) make mask
      pts1 = pts - pts.min(axis=0)
      mask = np.zeros(croped.shape[:2], np.uint8)
      cv2.drawContours(mask, [pts1], -1, (255, 255, 255), -1, cv2.LINE_AA)
  ## (3) do bit-op
      dst = cv2.bitwise_and(croped, croped, mask=mask)
  ## (4) add the white background
      bg = np.ones_like(croped, np.uint8) * 255
      cv2.bitwise_not(bg, bg, mask=mask)
      dst2 = bg + dst
  # cv2.imshow("croped.png", croped)
  # cv2.imshow("mask.png", mask)
  # cv2.imshow("dst.png", dst)
  # cv2.imshow("dst2.png", dst2)
      warped = four_point_transform(dst2, pts)
  return A_list, xml, data_big
  # for i in range(len(A_list)):
  #   with open(f"/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/Occupied/Oc{i}.jpg", "wb") as ee:
  #     ee.write(A_list[i])

  # show the original and warped images
  #     if occupied == 0:
  #       main_iter = main_iter + 1
  #       cv2.imwrite("/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotNew/" + repr(main_iter) + ".jpg", dst2)
  #     else:
  #       main_iter_oc = main_iter_oc + 1
  #       cv2.imwrite("/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotD/Ocupied/Oc" + repr(main_iter_oc) + ".jpg", dst2)
  #       cv2.imshow("Warped", warped)
  # # cv2.imwrite('D:\PKLotD\image_masked.png', masked_image)
  #     pts = np.empty([2, 0])

def xml_Bimg(event, context):
  A, xml, data_big = ananas()
  ad = {1:A, 2:xml, 3:str(data_big)}
  # for i in range(len(A)):
  #   with open(f"/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/PKLotA/Occupied/Oc{i}.jpg", "wb") as ee:
  #     ee.write(A[i])
  return ad

# if __name__ == "__main__":
#   A, xml, data_big = ananas()
#   ad = {1:A, 2:xml, 3:str(data_big)}
#   print(json.dumps(ad))
  # for i in range(len(gg)):
  #   with open(f"/home/dannobot/Work/sls/freeps/dev_freePS/xml_fucker/Oc{i}.jpg", "wb") as ee:
  #     ee.write(gg[i])
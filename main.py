import torch
import tele_bot as bot
import time
import cv2 as cv
import multiprocessing as mp

from flask import Flask, Response

def put_bath_to_queue(queue):
    try:
        vid = cv.VideoCapture('rtsp://admin:admin@192.168.1.10:1935')
        vid_batch = []

        print('Into stream')
        
        while(vid.isOpened()):
            ret, frame = vid.read()
            if ret:
                vid_batch.append(frame)
                # cv.imshow('Home', frame)
                # cv.waitKey(1)
            else:
                break        
            if len(vid_batch) >= 24:
                queue.put((vid_batch, time.ctime()))
                vid_batch = []

            if queue.qsize() > MAX_SIZE:
                queue.get()
    except Exception as ex:
        print('Err: ', str(ex))
    finally:
        vid.release()
        cv.destroyAllWindows()

MAX_SIZE = 9000

def detection(queue):

    model_onnx = torch.hub.load('./yolov5', 'custom', path='./exp/yolov5n.onnx', source='local', device='cpu')
    model_onnx.classes = [0]

    detection_list = []
    should_send_noti = True
    has_obj = False

    while True:
        vid_batch, c_time = queue.get()
        vid_batch = vid_batch[::3]
        res = model_onnx(vid_batch)

        res_batch = all([bool(len(r)) for r in res.xyxy])

        for i, img in enumerate(res.xyxy):
            has_obj = False if len(img) <= 0 else True
            img_ = vid_batch[i]

            if (not has_obj) and (not should_send_noti):
                should_send_noti = True

            for obj in img:
                x_min, y_min = int(obj[0].item()), int(obj[1].item())
                x_max, y_max = int(obj[2].item()), int(obj[3].item())

                img_ = cv.rectangle(img_, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)
            
            if has_obj:    
                detection_list.append(img_)

            if should_send_noti and has_obj and res_batch:
                should_send_noti = False
                
                name = time.time_ns()
                res = cv.imwrite(f'./out/{name}.jpg', img_)

                if res:
                    bot.send_noti(f'./out/{name}.jpg', c_time)

app = Flask(__name__)

def get_frame(queue):
    while True:
        video_batch, _ = queue.get()
        for frame in video_batch:
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route('/')
def video_stream():
    return Response(get_frame(queue), mimetype='multipart/x-mixed-replace; boundary=frame')
    

if __name__ == "__main__":

    queue = mp.Queue()

    p1 = mp.Process(target=put_bath_to_queue, args=(queue,))  
    p2 = mp.Process(target=detection, args=(queue,))

    p1.start()
    p2.start()

    app.run()


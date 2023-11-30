# Human Intrusion Detection System

![Demo](https://github.com/ChiThang-50Cent/human-detection/blob/main/screen-capture.gif)

## Giới thiệu

Repo này tập trung vào việc phát triển một hệ thống phát hiện xâm nhập dựa trên luồng video trực tiếp từ camera (giao thức RTSP). Xử lý bằng máy tính có hiệu năng thấp, đặc biệt được thiết kế để sử dụng trên các thiết bị như máy thu ngân. Hệ thống này có khả năng hiển thị video real-time với độ trễ khoảng 1-2 giây và hỗ trợ gửi thông báo qua tin nhắn Telegram khi phát hiện sự xâm nhập.

## Đặc điểm chính

- Đọc luồng video trực tiếp từ camera (RTSP)
- Sử dụng mô hình YOLOv5n để phát hiện và nhận diện người trong video.
- Train mô hình dưới bộ dữ liệu chứa khoảng 2000 ảnh người được trích từ dataset COCO.
- Áp dụng kỹ thuật multiprocess để giảm độ trễ trong việc stream video real-time và phát hiện xâm nhập.
- Sử dụng Flask để hiển thị video trên Web

## Cài đặt và Sử dụng

0. **Cài đặt các package cần thiết** 
   - Có thể cài dặt các pakage theo file requeriment ở folder yolov5
   - Cài thêm pakage để đọc config từ file .env và Flask để stream video lên web
  
1. **Tạo dataset từ COCO**
   - Sử dụng dataset COCO trên Kaggle, tách những ảnh có *classes person* để train mô hình.
    
2. **Train YOLOv5n**
   - Sử dụng GPU free trên Kaggle, huấn luyện mô hình YOLO, nếu như máy inference đủ mạnh, có thể sử dụng các scale khác của mô hình như là s, l, etc.  

3. **Cấu hình Telegram**:
   - Đăng ký bot với Telegram và lấy API key.
   - Cung cấp thông tin API key trong file cấu hình.

4. **Khởi động hệ thống**:
   - Chạy lệnh `python main.py` để bắt đầu streaming và phát hiện xâm nhập.

## Demo
Một số hình ảnh thông báo nhận được khi có người được phát hiện.</br>
![image](https://github.com/ChiThang-50Cent/human-detection/assets/62085284/81296e11-4ace-4ddb-939c-15d347aee11e)
![image](https://github.com/ChiThang-50Cent/human-detection/assets/62085284/7d978fab-85ab-4dd5-bc1f-ce0186ff0247)


from flask import Blueprint, Response, request, jsonify
from flask_cors import CORS
import cv2
import os
import pandas as pd
import datetime
import numpy as np
import time
from ultralytics import YOLO
import serial

home_bearing = Blueprint('bearing_routes', __name__)
CORS(home_bearing)

#definisi variabel global untuk flags
inspectionFlag = False
bearing_detected = False
resetInspectionFlag = True
#definisi variabel global untuk
latest_frame = None
updateData = {'total_judges': 0,
              'sesion_judges': 0,
              'trigger_start': 0,
              'trigger_reset':0,
              'last_judgement': 'NG',
              'img_path' : '',
              'arduino_connected': False,
              }

model = YOLO("./models/yolov8m.pt")

############## function untuk arduino communication #########
def init_serial_connection():
    global arduino
    while True:
        print("init_serial_connection called")
        try:
            arduino = serial.Serial('/dev/arduino', 115200, timeout=0.1)  # Initialize the Arduino port with shorter timeout
            if arduino.isOpen():  # Check if the serial port is open
                arduino.close()  # Close the port if it is open
            arduino.open()  # Reopen the serial port
            print("Connection established.")
            
            #update flag arduino connected
            update_data_dict('arduino_connected', True)
            
            break  # Exit the loop if successful
        except serial.SerialException as e:
            #update flag arduino conection
            update_data_dict('arduino_connected', False)
            
            print(f"Serial connection error during initialization: {e}")
            print("Waiting for connection...")
            time.sleep(5)  # Wait for 5 seconds before trying again

def baca_data_arduino():
    global arduino, inspectionFlag, resetInspectionFlag
    while True:
        try:
            input_data = arduino.readline().strip().decode('utf-8')
            if input_data == "start_scan":
                print(f"FROM ARDUINO: {input_data}")
                inspectionFlag = True
                update_data_dict('trigger_start', True)
                break
            elif input_data == "reset_scan":
                print(f"FROM ARDUINO: {input_data}")
                resetInspectionFlag = True
                inspectionFlag = False
                update_data_dict('trigger_reset', True)
                break
            else:
                update_data_dict('trigger_start', False)
                update_data_dict('trigger_reset', False)
                print(f"FROM ARDUINO: {input_data}")
                break
        except serial.SerialException:
            print("Serial connection error. Waiting for reconnection...")
            arduino.close()
            init_serial_connection()  # Reinitialize the serial connection
        except UnicodeDecodeError:
            print("Error decoding input data.")
############## end of function untuk arduino communication #########
    
    

############## function untuk stream frame ke client ################
def stream_video(device):
    global latest_frame, bearing_detected, inspectionFlag, updateData, resetInspectionFlag
    time.sleep(2)
    cap = cv2.VideoCapture(device)
    
    if not cap.isOpened():
        # Generate a placeholder frame with error message
        error_frame = np.zeros((500, 800, 3), np.uint8)
        pesan_string = f'''Camera index {device} out of range
                            Silahkan tekan Refresh Camera atau Halaman Web
                            jika masih berlanjut Lepas pasang USB pada Camera
                            jika masih error lambaikan tangan pada kamera'''
        cv2.putText(error_frame, pesan_string, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        ret, buffer = cv2.imencode('.jpg', error_frame)
        error_frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + error_frame + b'\r\n')
    
    # Set frame width and height for 16:9 aspect ratio and 1080p resolution
    frame_width = 720
    frame_height = 480  # Initial frame height for 16:9 aspect ratio and 720p resolution

    # Calculate the frame width based on the aspect ratio
    frame_width = int((frame_height / 9) * 16)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Tidak dapat membaca frame")
            break
        results = model(frame, conf=0.9, classes=0)
        annotated_frame = results[0].plot()
                    
        # dibawah ini logika untuk memperkecil ukuran frame agar ringan saat di show up
        #Set frame width and height for 16:9 aspect ratio and 1080p resolution
        frame_width = 1280
        frame_height = 720  # Initial frame height for 16:9 aspect ratio and 720p resolution

        # Calculate the frame width based on the aspect ratio
        frame_width = int((frame_height / 9) * 16)
        annotated_frame = cv2.resize(annotated_frame, (int(frame_width * (810 / frame_height)), 810))
        
        #encoding gambar yang akan di kirim  menjadi jpg
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        
        #read arduino data serial
        baca_data_arduino()
        
        print ("flag status", resetInspectionFlag, inspectionFlag)
        #jika trigger untuk deteksi on
        if inspectionFlag and resetInspectionFlag:
            print("ini didalam if scann")
        # logika untuk mendapatkan data object yang di deteksi
        #kemudian perbarui nilai di global variabel bearing_detected
            for r in results:
                detected_object = len(r.boxes.cls)
                if detected_object:
                    bearing_detected = True
                    save_image(annotated_frame, 'GOOD', 'Deteksi_oke')
                    print(f'Detected object: {detected_object}')
                    latest_frame = frame
                    resetInspectionFlag = False
                else:
                    bearing_detected = False
                    print('No bearing object detected')
                    save_image(annotated_frame, 'NG', 'Tidak_terdeteksi')
                    print(f'Detected object: {detected_object}')
                    latest_frame = frame
                    resetInspectionFlag = False
            
            update_data_dict('last_judgement', bearing_detected)
            update_data_dict('sesion_judges', updateData['sesion_judges']+1)
      
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()


############## Function untuk start inspection #################
def start_inspection():
    global inspectionFlag
    inspectionFlag = True
    return 

############## Function untuk save images #################
def save_image(images_to_save, raw_file_name, image_category):
    corrected_name = raw_file_name.replace(' ', '_')

    # Get current date and time for saving the file name.
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{corrected_name}_{timestamp}"
    
    # Buat Direktory download
    current_directory = os.path.dirname(os.path.abspath(__file__))
    downloads_directory = os.path.join(current_directory, f'Downloads/{image_category}')
    os.makedirs(downloads_directory, exist_ok=True)
    
    #simpan ke direktori download
    image_path = os.path.join(downloads_directory, f"{file_name}.jpg")  # Menambahkan timestamp pada nama file
    
    cv2.imwrite(image_path, images_to_save)
    print(f"Gambar disimpan di {image_path}")
    
    # Update judgment.csv file with the new data.
    function_update_csv(image_path, file_name)
    

def function_update_csv(pathImg, filename):
    global updateData
    
    df = pd.read_csv("judgement.csv")
    id_terakhir = df['inspection_id'].iloc[-1]
    
    result, date, time= filename.split('_')
    
    id_terakhir += 1
    
    update_data_dict('total_judges', int(id_terakhir))
    
    new_data= {
        "inspection_id" : int(id_terakhir),
        "inspection_date" : int(date),
        "inspection_time" : int(time),
        "inspection_result" : result,
        "image_path" : pathImg
    }
    
    new_row = pd.DataFrame([new_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("judgement.csv", index=False)
    print("Data has been updated in judgement.csv")
    
        
        
############## Function untuk menampilkan last detection #################
def last_detection():
    global latest_frame
    while True:
        if latest_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
        else:
            # Generate a placeholder frame with a message if no frame is available
            placeholder_frame = np.zeros((500, 800, 3), np.uint8)
            message = "No frame available"
            cv2.putText(placeholder_frame, message, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buffer = cv2.imencode('.jpg', placeholder_frame)
            placeholder_frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + placeholder_frame + b'\r\n')
        time.sleep(0.1)  # Add a small delay to avoid high CPU usage

############## Function untuk update data #################
def update_data_dict(key, value):
    global updateData
    updateData[key] = value
    

####################### END POINT ##########################
@home_bearing.route('/bearing/show-video', methods=['GET'])
def home_show_video():
    id_camera = request.args.get('id_camera', default=2, type=int)
    init_serial_connection()
    print(f'Settings show video with camera index {id_camera}')
    return Response(stream_video(id_camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@home_bearing.route('/bearing/last_detections', methods=['GET'])
def home_show_last():
    return Response(last_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

@home_bearing.route('/bearing/get-data', methods=['GET'])
def get_data():
    global bearing_detected
    data = updateData
    print(data['total_judges'])
    # data = {'bearing_detected': bearing_detected}
    return jsonify(data)

@home_bearing.route('/bearing/start', methods=['GET'])
def startInspection():
    start_inspection()
    return "sucess startingspection"
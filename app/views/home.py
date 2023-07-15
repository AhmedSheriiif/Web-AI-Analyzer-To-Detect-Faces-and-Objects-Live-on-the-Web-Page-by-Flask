import datetime
import time

import cv2
from flask import Blueprint, render_template, request, send_from_directory, session, jsonify, json, Response, redirect
from werkzeug.utils import secure_filename
from app.models.my_data import Images, Cameras, Videos, Events

from ..models import db
from .. import app
import os
from os.path import join, dirname, realpath
import validators

# AI MODELS
import YoloDetector
import EmotionDetector

home = Blueprint('home', __name__)

USER_EMAIL = ""

# PATHS
UPLOADS_PATH = join(dirname(realpath(__file__)), '../static/user_data/uploads_emotion_detection/..')
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

app_root = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(app_root, '../static/user_data/uploads_object_detection/')
target2 = os.path.join(app_root, '../static/user_data/uploads_emotion_detection/')
if not os.path.isdir(target):
    os.makedirs(target)

if not os.path.isdir(target2):
    os.makedirs(target2)

######################## YOLO VARIABLES ###################################
WEIGHTS = "yolov7.pt"
PRED_LOCATION = os.path.join(app_root, '../static/user_data/predicts_object_detection/')
YOLO = YoloDetector.YoloDetectorClass(project=PRED_LOCATION)
YOLO_LOADED = False
Video_Name = ""
CameraLinks = []

###################### EMOTION VARIABLES #####################################
EMOTION_PATH = "cnn.hdf5"
DETECTION_PATH = "haarcascade_frontalface_default.xml"
EMO_PRED_LOCATION = os.path.join(app_root, '../static/user_data/predicts_emotion_detection/')
EMO = EmotionDetector.EmotionDetectorClass(detection_model_path=DETECTION_PATH, emotion_model_path=EMOTION_PATH,
                                           detected_img_path=EMO_PRED_LOCATION)
EMO_LOADED = False
EMO_Video_Name = ""
EMO_CameraLinks = []

ModelSelected = ""


################################################################################

#########################################################  SHOWING LIVE VIDEOS ##############################################################
########################################################## WORKING WITH YOLO ################################################################
##### VIDEO PATH
def infer_video(video_name):
    user_mail = USER_EMAIL

    # Loading YOLO
    global YOLO_LOADED
    if not YOLO_LOADED:
        YOLO.Load_Model()
        YOLO_LOADED = True

    count = 0
    Vid_Path = os.path.join(target, video_name)
    video = cv2.VideoCapture(Vid_Path)
    w = int(video.get(3))
    h = int(video.get(4))

    FPS = 10
    Writer_Path = os.path.join(PRED_LOCATION, video_name)
    Vid_Writer = cv2.VideoWriter(Writer_Path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (w, h))

    MyVid = Videos.query.filter_by(name=video_name).first()
    Vid_ID = MyVid.id

    Frame_Count = 0
    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            Frame_Location = r'{}/{}__{}.png'.format(PRED_LOCATION, video_name, count)
            cv2.imwrite(Frame_Location, frame)
            det_frame, detections = YOLO.Run_Detect(source=Frame_Location)

            Vid_Writer.write(det_frame)

            ret, buffer = cv2.imencode('.jpg', det_frame)
            frame = buffer.tobytes()
            if detections:
                detections = detections[0]
                detections_splitted = detections.split(',')
                detections = " , ".join(detections_splitted)

                # Adding the Event to the Database
                new_event = Events(email=user_mail, model="Object Detection", source="Video", source_name=video_name,
                                   message=detections, event_date=str(datetime.datetime.now()),
                                   event_link="{}__{}.png".format(video_name, count))
                db.session.add(new_event)
                db.session.commit()

            Frame_Count += 10  # i.e. at 30 fps, this advances one second
            video.set(cv2.CAP_PROP_POS_FRAMES, Frame_Count)

        count += 1

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/videos_feed")
def video_feed():
    if session.get('email') is None:
        login_problem = "Sorry, you have to login first to use our service.."
        return render_template('auth/login.html', login_problem=login_problem)

    else:
        global USER_EMAIL
        USER_EMAIL = session['email']
        return Response(infer_video(Video_Name),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


##### CAMERAS
def Pred_One_Camera(camera_link, CameraLinkName):
    user_mail = USER_EMAIL

    # Loading YOLO
    global YOLO_LOADED
    if not YOLO_LOADED:
        YOLO.Load_Model()
        YOLO_LOADED = True

    video = cv2.VideoCapture(camera_link)
    w = int(video.get(3))
    h = int(video.get(4))
    FPS = 10
    Writer_Path = os.path.join(PRED_LOCATION, CameraLinkName + ".mp4")
    Vid_Writer = cv2.VideoWriter(Writer_Path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (w, h))
    count = 0
    CamID = Cameras.query.filter_by(link=camera_link).order_by(Cameras.id.desc()).first().id
    print(CamID)
    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            Frame_Location = r'{}/{}__{}.png'.format(PRED_LOCATION, CameraLinkName, count)
            cv2.imwrite(Frame_Location, frame)
            det_frame, detections = YOLO.Run_Detect(source=Frame_Location)
            Vid_Writer.write(det_frame)

            ret, buffer = cv2.imencode('.jpg', det_frame)
            frame = buffer.tobytes()

            if detections:
                detections = detections[0]
                detections_splitted = detections.split(',')
                detections = " , ".join(detections_splitted)
                new_event = Events(email=user_mail, model="Object Detection", source="Camera", source_name=camera_link,
                                   message=detections, event_date=str(datetime.datetime.now()),
                                   event_link="{}__{}.png".format(CameraLinkName, count))

                db.session.add(new_event)
                db.session.commit()

        count += 1
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/cameras_feed/<int:id>/")
def camera_feed(id):
    if session.get('email') is None:
        login_problem = "Sorry, you have to login first to use our service.."
        return render_template('auth/login.html', login_problem=login_problem)
    else:
        global USER_EMAIL
        USER_EMAIL = session['email']
        timestamp = int(time.time())
        CameraLinkName = "CamLink{}_{}".format(id, timestamp)

        if ModelSelected == "Object Detection":
            return Response(Pred_One_Camera(CameraLinks[id], CameraLinkName),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

        elif ModelSelected == "Emotion Detection":
            return Response(Pred_One_Camera_emo(CameraLinks[id], CameraLinkName),
                            mimetype='multipart/x-mixed-replace; boundary=frame')


###################### WORKING WITH EMO ############################
#### VIDEO
def infer_video_emo(video_name):
    user_mail = USER_EMAIL

    # Loading EMO
    global EMO_LOADED
    if not EMO_LOADED:
        EMO.Load_Model()
        EMO_LOADED = True

    count = 0
    Vid_Path = os.path.join(target2, video_name)
    video = cv2.VideoCapture(Vid_Path)
    w = int(video.get(3))
    h = int(video.get(4))
    FPS = 5
    print("111111")
    Writer_Path = os.path.join(EMO_PRED_LOCATION, video_name)
    Vid_Writer = cv2.VideoWriter(Writer_Path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (w, h))

    MyVid = Videos.query.filter_by(name=video_name).first()
    Vid_ID = MyVid.id

    Frame_Count = 0
    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            Frame_Location = r'{}/{}__{}.png'.format(EMO_PRED_LOCATION, video_name, count)
            cv2.imwrite(Frame_Location, frame)
            Saving_Name = r'{}__{}.png'.format(video_name, count)
            det_frame, detections = EMO.Run_Detect(source=Frame_Location, saving_name=Saving_Name)

            Vid_Writer.write(det_frame)

            ret, buffer = cv2.imencode('.jpg', det_frame)
            frame = buffer.tobytes()
            if detections:
                new_event = Events(email=user_mail, model="Emotion Detection", source="Video", source_name=video_name,
                                   message=detections, event_date=str(datetime.datetime.now()),
                                   event_link="{}__{}.png".format(video_name, count))
                db.session.add(new_event)
                db.session.commit()

            Frame_Count += 10  # i.e. at 30 fps, this advances one second
            video.set(cv2.CAP_PROP_POS_FRAMES, Frame_Count)
        count += 1

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/videos_feed_emo")
def video_feed_emo():
    if session.get('email') is None:
        login_problem = "Sorry, you have to login first to use our service.."
        return render_template('auth/login.html', login_problem=login_problem)
    else:
        global USER_EMAIL
        USER_EMAIL = session['email']
        return Response(infer_video_emo(Video_Name),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


#### CAMERAS
def Pred_One_Camera_emo(camera_link, CameraLinkName):
    user_mail = USER_EMAIL

    # Loading YOLO
    global EMO_LOADED
    if not EMO_LOADED:
        EMO.Load_Model()
        EMO_LOADED = True

    video = cv2.VideoCapture(camera_link)
    w = int(video.get(3))
    h = int(video.get(4))
    FPS = 10

    Writer_Path = os.path.join(EMO_PRED_LOCATION, CameraLinkName + ".mp4")
    Vid_Writer = cv2.VideoWriter(Writer_Path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (w, h))
    count = 0
    CamID = Cameras.query.filter_by(link=camera_link).order_by(Cameras.id.desc()).first().id

    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            Frame_Location = r'{}/{}__{}.png'.format(EMO_PRED_LOCATION, CameraLinkName, count)
            cv2.imwrite(Frame_Location, frame)
            Saving_Name = r'{}__{}.png'.format(CameraLinkName, count)
            det_frame, detections = EMO.Run_Detect(source=Frame_Location, saving_name=Saving_Name)

            Vid_Writer.write(det_frame)

            ret, buffer = cv2.imencode('.jpg', det_frame)
            frame = buffer.tobytes()

            if detections:
                detections = detections[0]
                new_event = Events(email=user_mail, model="Emotion Detection", source="Camera", source_name=camera_link,
                                   message=detections, event_date=str(datetime.datetime.now()),
                                   event_link="{}__{}.png".format(CameraLinkName, count))

                db.session.add(new_event)
                db.session.commit()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


######################################################### ROUTES ####################################################
# HOME PAGE
@home.route('/home')
def home_page():
    # Check if user is logged in
    if session.get('email') is None:
        login_problem = "Sorry, you have to login first to use our service.."
        return render_template('auth/login.html', login_problem=login_problem)

    else:
        user_mail = session['email']
        user_fullname = session['fullname']

        # Events Table Data
        table_data = []
        # 1- Getting Events and Storing in the Table of Data
        UserEvents = Events.query.filter_by(email=user_mail)
        for event in UserEvents:
            data = {"ID": event.id, "Model": event.model, "Source": event.source, "Source_Name": event.source_name,
                    "Messages": event.message, "Date": event.event_date, "Link": event.event_link}
            table_data.append(data)

        #############################
        # Solid Line DATA
        solid_labels = []
        solid_data = []
        if len(table_data) > 0:
            min_date = min(table_data, key=lambda x: x['Date'])["Date"]
            max_date = max(table_data, key=lambda x: x['Date'])["Date"]
            current_date = min_date
            while current_date <= max_date:
                events_betn = list(filter(lambda x: min_date <= x['Date'] <= current_date, table_data))
                solid_labels.append(current_date.strftime('%m-%d %H:%M'))
                solid_data.append(len(events_betn))
                current_date = current_date + datetime.timedelta(hours=1)

        solid_dict = {
            "data": solid_data,
            "labels": solid_labels,
            "title": 'Events per Time',
            "data_unit": "Events",
            "min_unit": 0,
            "unit_label": ""
        }

        ################################
        # Score Data
        no_cameras = Cameras.query.filter_by(email=user_mail).count()
        no_videos = Videos.query.filter_by(email=user_mail).count()
        score_dict = {
            "no_events": len(table_data),
            "no_models": 2,
            "no_cameras": no_cameras,
            "no_videos": no_videos
        }
        return render_template("home/home.html",
                               solid_line=solid_dict, score=score_dict, table_data=table_data,
                               myemail=user_mail, fullname=user_fullname)


# Welcome (Login Page)
@home.route('/')
def welcome_page():
    return redirect('/home')


## Page of ANALYTICS (CHOOSING MODEL AND METHOD)
# - Once user choose model --> Model will be Loaded
@home.route('/analytics', methods=['GET', 'POST'])
def analytic_page():
    if session.get('email') is None:
        login_problem = "Sorry, you have to login first to use our service.."
        return render_template('auth/login.html', login_problem=login_problem)

    else:
        user_fullname = session['fullname']
        user_mail = session['email']
        global ModelSelected

        if request.method == 'GET':
            return render_template('home/Analytics.html', myemail=user_mail, fullname=user_fullname)

        else:
            # Choosing YOLO:
            if request.form.get('model') == 'object_detection':
                global YOLO_LOADED
                if not YOLO_LOADED:
                    YOLO.Load_Model()
                    YOLO_LOADED = True
                ModelSelected = "Object Detection"

            elif request.form.get('model') == "emotion_detection":
                global EMO_LOADED
                if not EMO_LOADED:
                    EMO.Load_Model()
                    EMO_LOADED = True
                ModelSelected = "Emotion Detection"

            # Image
            if request.form['source'] == 'image':
                return render_template('home/uploadImage.html', myemail=user_mail, fullname=user_fullname,
                                       model=ModelSelected)
            # Video
            elif request.form['source'] == 'video':
                return render_template('home/uploadvedio.html', myemail=user_mail, fullname=user_fullname,
                                       model=ModelSelected)
            # Camera
            else:
                return render_template('home/uploadcam.html', myemail=user_mail, fullname=user_fullname,
                                       model=ModelSelected)


# Object Detection Page
@home.route('/object_det')
def object_page():
    if session.get('email') is None:
        return render_template('error/notfound.html')
    else:
        myname = session['username']
        myemail = session['email']
        firstname = session['firstname']
        return render_template('home/objectDet.html', myname=myname, myemail=myemail, firstname=firstname)


# Emotion Detection Page
@home.route('/emotion_det')
def emotion_page():
    if session.get('email') == None:
        return render_template('error/notfound.html')
    else:
        myname = session['username']
        myemail = session['email']
        firstname = session['firstname']

        return render_template('home/emotionalDet.html', myname=myname, myemail=myemail, firstname=firstname)


############################################### GETTING FILES SRCs FUNCTIONS #############################
# Static/Upload  --> YOLO UPLOADED FILES
@app.route('/file/<filename>')
def get_image(filename):
    return send_from_directory(target, filename)


# Static2/Upload2  --> EMO UPLOADED FILES
@app.route('/file2/<filename>')
def get_image2(filename):
    return send_from_directory(target2, filename)


# Image PREDICTED Locations
@app.route('/file3/<filename>')
def get_predict(filename):
    if ModelSelected == "Object Detection":
        return send_from_directory(PRED_LOCATION, filename)
    elif ModelSelected == "Emotion Detection":
        return send_from_directory(EMO_PRED_LOCATION, filename)


# Static2/Predicts2  --> EMO PREDICTED FILES
@app.route('/file4/<filename>')
def get_predict2(filename):
    return send_from_directory(EMO_PRED_LOCATION, filename)


######################################################### UPLOADING IMGS, VIDEOS, Picking CAMERAS ###########################################
#### UPLOADING AND DETECTING IMAGE #####
@home.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if session.get('email') is None:
        login_problem = "Sorry, you have to login first to use our service.."
        return render_template('auth/login.html', login_problem=login_problem)

    else:
        prediction = 0
        user_fullname = session['fullname']
        user_mail = session['email']

        if request.method == 'GET':
            return render_template('home/uploadImage.html', prediction=prediction, myname=user_fullname,
                                   myemail=user_mail)

        else:
            myimage = request.files['image']
            filename = secure_filename(myimage.filename)
            if ModelSelected == "Object Detection":
                destination = '/'.join([target, filename])
            else:
                destination = '/'.join([target2, filename])

            myimage.save(destination)  # Saved the uploaded image

            if not myimage:
                uploadimg = 'please upload an image'
                return render_template('home/uploadImage.html', prediction=prediction, uploadimg=uploadimg,
                                       myname=user_fullname, myemail=user_mail)

            else:
                # Adding Image to the DB
                filename = secure_filename(myimage.filename)
                mimetype = myimage.mimetype
                newimage = Images(email=user_mail, model=ModelSelected, mimetype=mimetype, name=filename,
                                  img=myimage.read())
                db.session.add(newimage)
                db.session.commit()
                id = newimage.id
                uploaded = 'your image uploaded successfully'
                myimage = Images.query.filter_by(id=id).first()
                filename = myimage.name

                if ModelSelected == "":
                    return render_template("home/Analytics.html", myemail=user_mail, fullname=user_fullname)

                else:
                    prediction = 1
                    detections = ""

                    if ModelSelected == "Object Detection":
                        # Loading YOLO
                        global YOLO_LOADED
                        if not YOLO_LOADED:
                            YOLO.Load_Model(weights=WEIGHTS)
                            YOLO_LOADED = True

                        detected_img, detections = YOLO.Run_Detect(source=destination)
                        if detections:
                            detections = detections[0]
                            detections = detections.split(',')
                        else:
                            detections = ["No Detections"]

                        EventLink = r"predicts_object_detection/{}".format(filename)

                    elif ModelSelected == "Emotion Detection":
                        global EMO_LOADED
                        if not EMO_LOADED:
                            EMO.Load_Model()
                            EMO_LOADED = True
                        detected_img, detections = EMO.Run_Detect(source=destination, saving_name=filename)
                        if detections is None:
                            detections = "No Detections"
                        EventLink = r"predicts_emotion_detection/{}".format(filename)

                    NewEvent = Events(email=user_mail, model=ModelSelected, source="Image", source_name=filename,
                                      event_date=str(datetime.datetime.now()), message=", ".join(detections),
                                      event_link=EventLink)
                    db.session.add(NewEvent)
                    db.session.commit()

                    return render_template('home/uploadImage.html', prediction=prediction, detections=detections,
                                           filename=filename, uploaded=uploaded, myname=user_fullname,
                                           myemail=user_mail)


#### UPLOADING VIDEO
@home.route('/upload_vedio', methods=['GET', 'POST'])
def upload_vedio():
    prediction = 0
    if session.get('email') is None:
        login_problem = "Sorry, you have to login first to use our service.."
        return render_template('auth/login.html', login_problem=login_problem)

    else:
        myname = session['fullname']
        myemail = session['email']

        if request.method == 'GET':
            return render_template('home/uploadvedio.html', prediction=prediction, myname=myname,
                                   myemail=myemail)
        else:
            global Video_Name
            myved = request.files['video']
            filename = secure_filename(myved.filename)
            timestamp = int(time.time())
            [video, extension] = filename.split('.')
            Video_Name = "{}_{}.{}".format(video, timestamp, extension)

            if ModelSelected == "Object Detection":
                destination = '/'.join([target, Video_Name])
            else:
                destination = '/'.join([target2, Video_Name])

            myved.save(destination)
            if not myved:
                uploadvedio = 'please upload a video'
                return render_template('home/uploadvedio.html', prediction=prediction, uploadvedio=uploadvedio,
                                       myname=myname, myemail=myemail)
            else:
                if ModelSelected == "":
                    return render_template("home/Analytics.html", myemail=myemail, fullname=myname)

                else:
                    source_name = secure_filename(myved.filename)
                    NewVideo = Videos(name=Video_Name, email=myemail, model=ModelSelected)
                    db.session.add(NewVideo)
                    db.session.commit()
                    prediction = 1
                    uploaded = 'your video uploaded successfully'

                return render_template('home/uploadvedio.html', prediction=prediction, uploaded=uploaded, myname=myname,
                                       myemail=myemail, model=ModelSelected, source_name=Video_Name)


############# UPLOAD CAMERA LINKS #######################
### YOLO
@home.route('/upload_link', methods=['GET', 'POST'])
def upload_link():
    if session.get('email') is None:
        login_problem = "Sorry, you have to login first to use our service.."
        return render_template('auth/login.html', login_problem=login_problem)

    else:
        myname = session['fullname']
        myemail = session['email']
        flag1 = 0

        if request.method == 'GET':
            return render_template('home/uploadcam.html', flag1=flag1, myname=myname, myemail=myemail)

        else:
            stream_url = request.form['stream_url']
            location = request.form['location']
            camera_name = request.form['camera_name']

            NewCamera = Cameras(email=myemail, link=stream_url, name=camera_name, location=location,
                                model=ModelSelected)
            db.session.add(NewCamera)
            db.session.commit()
            flag1 = 1
            uploaded = 'your link uploaded successfully , add a new one'
            return render_template('home/uploadcam.html', flag1=flag1, uploaded=uploaded, myname=myname,
                                   myemail=myemail)


### LOADING CAMERAS TO PREDICT
## YOLO
@home.route('/predict_link')
def predict_link():
    if session.get('email') is None:
        login_problem = "Sorry, you have to login first to use our service.."
        return render_template('auth/login.html', login_problem=login_problem)

    else:
        myname = session['fullname']
        myemail = session['email']

        MyCameraLinks = Cameras.query.filter_by(email=myemail, model=ModelSelected)
        global CameraLinks
        CameraLinks = []
        for Camera in MyCameraLinks:
            CameraLinks.append(Camera.link)
        return render_template('home/predictcam.html', model=ModelSelected, CamLinks=MyCameraLinks, myemail=myemail,
                               myname=myname)








@home.route('/video_events/<source_name>')
def video_events(source_name):
    myname = session['fullname']
    myemail = session['email']
    return render_template('home/videoEvents.html', myname=myname, myemail=myemail, source_name=source_name)


@home.route('/get_video_events/<source_name>')
def get_video_events(source_name):
    CurrentEvents = Events.query.filter_by(source_name=source_name)

    ids = []
    models = []
    sources = []
    source_names = []
    messages = []
    dates = []
    links = []

    if CurrentEvents:
        for event in CurrentEvents:
            ids.append(event.id)
            models.append(event.model)
            sources.append(event.source)
            source_names.append(event.source_name)
            messages.append(event.message)
            dates.append(event.event_date)
            links.append(event.event_link)

        return jsonify({"IDS": ids,
                        "MODELS": models,
                        "SOURCES": sources,
                        "SOURCE_NAMES": source_names,
                        "MESSAGES": messages,
                        "DATES": dates,
                        "LINKS": links,
                        "error": "data"})
    else:
        return jsonify({"error": "no data"})


@home.route('/camera_events/<int:id>')
def camera_events(id):
    if session.get('email') is not None:
        myname = session['fullname']
        myemail = session['email']

        Camera = Cameras.query.filter_by(id=id).first()
        CamLink = Camera.link
        CamEvents = Events.query.filter_by(source_name=CamLink)
        return render_template('home/cameraEvents.html', myevnts=CamEvents, myname=myname, myemail=myemail, camera_id=id)
    else:
        return render_template('error/notfound.html')


@home.route('/get_camera_events/<int:id>')
def get_camera_events(id):
    Camera = Cameras.query.filter_by(id=id).first()
    CamLink = Camera.link
    CurrentEvents = Events.query.filter_by(source_name=CamLink)

    ids = []
    models = []
    sources = []
    source_names = []
    messages = []
    dates = []
    links = []

    if CurrentEvents:
        for event in CurrentEvents:
            ids.append(event.id)
            models.append(event.model)
            sources.append(event.source)
            source_names.append(event.source_name)
            messages.append(event.message)
            dates.append(event.event_date)
            links.append(event.event_link)

        return jsonify({"IDS": ids,
                        "MODELS": models,
                        "SOURCES": sources,
                        "SOURCE_NAMES": source_names,
                        "MESSAGES": messages,
                        "DATES": dates,
                        "LINKS": links,
                        "error": "data"})
    else:
        return jsonify({"error": "no data"})


@home.route('/deleteCam/<int:id>')
def del_cam(id):
    Camera = Cameras.query.filter_by(id=id).first()
    CamLink = Camera.link

    Events.query.filter_by(source_name=CamLink).delete()
    Cameras.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect("/predict_link")


# STORAGE BUTTON
@home.route('/storage')
def storage():
    print("Opening Storage.....")
    return render_template("home/storage.html")


# All Events
@home.route('/all_events/')
def all_events():
    # Check if user is logged in
    if session.get('email') is None:
        login_problem = "Sorry, you have to login first to use our service.."
        return render_template('auth/login.html', login_problem=login_problem)

    else:
        user_mail = session['email']
        user_fullname = session['fullname']

        # Events Table Data
        table_data = []
        # 1- Getting Events and Storing in the Table of Data
        UserEvents = Events.query.filter_by(email=user_mail)
        for event in UserEvents:
            data = {"ID": event.id, "Model": event.model, "Source": event.source, "Source_Name": event.source_name,
                    "Messages": event.message, "Date": event.event_date, "Link":event.event_link}
            table_data.append(data)

        return render_template("home/all_events.html", table_data=table_data, myemail=user_mail, fullname=user_fullname)

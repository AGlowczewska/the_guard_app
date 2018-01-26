import cv2
from time import sleep

import firebase_admin
import argparse 
from google.cloud import storage
from firebase_admin import credentials, auth
import subprocess

def initialize_firebase_admin_sdk():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)


def recordVideo(stream, timestamp, time):

    initialize_firebase_admin_sdk()
    client = storage.Client()
 
    #client = storage.Client.from_service_account_json('serviceAccountKey.json')
    #buckets = list(client.list_buckets())
    #print(buckets)
    bucket = client.get_bucket('guardapp-ac65a.appspot.com')

    streamAddress = 'http://localhost:80/hls/'+stream+'.m3u8'
    fileDestination = 'static/recordings/recording'+str(timestamp)+'.avi'
    print("STREAM: {}\n".format(streamAddress))
    print("FILE: {}\n".format(fileDestination))
    cap = cv2.VideoCapture(streamAddress)
    size = (int(cap.get(3)),int(cap.get(4)))
    record = cv2.VideoWriter(fileDestination, cv2.VideoWriter_fourcc('M','J','P','G'), 30, size)
    fps = 30
    i = 0

    while cap.isOpened() and i < int(time)*fps:
        if i == 0:
            print("Recording started")
        isAvail, frame = cap.read()
        if isAvail:
            record.write(frame)
            sleep(1/fps)
        #print(" {} {} ".format(i, isAvail))
        i+=1

    cap.release()
    record.release()
    cv2.destroyAllWindows()
    print("Converting avi to mp4")

    subprocess.call(['bash','convert_video.sh',timestamp])

    #upload to bucket
    blob = bucket.blob(stream+'/'+timestamp+'.mp4')
    blob.upload_from_filename(filename=fileDestination)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("stream", help="Stream to record", type = str)
    parser.add_argument("timestamp", help="Timestamp of beginning of recording", type = str)
    parser.add_argument("time", help="How long you want to record the stream", type = str, default="30")
    args = parser.parse_args()




    recordVideo(args.stream, args.timestamp, args.time)

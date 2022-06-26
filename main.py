# Import Libraries.
from flask import Flask, render_template, request
import os, glob, shutil

# Import inference files, configured to run script on webcam and picture.
import detectvideo
import detect

# Loading Flask instance.
app = Flask(__name__)

# Each time we redirect our traffic to the "/video" directory from index.html (when we click the "webcam" button),
# we execute the inference for the webcam.
@app.route('/video', methods=['GET', 'POST'])
def video():
    detectvideo.main()
# Once the webcam is closed, we return the execution to the index.html file, with an example of an inference and the option
# to upload again another picture or open the webcam
    return render_template('index.html', file_clean='/static/school3.jpg',
                           file_tag='/static/school3.jpg2.jpg')

# If we select to upload a picture on index.html, we will be redirect here.
@app.route('/upload', methods=['GET', 'POST'])
def uploadfile():
    if request.method == 'POST':
        fichero=request.files['file']

# We save the uploaded file on the "static" directory before renaming the extension. The inference file needs jpg
# format instead of jpeg.

        file_changed=fichero.filename.replace(".jpeg",".jpg")
        fichero.save('static/'+ file_changed)


        #file=('static/' + fichero.filename.replace(".jpeg",".jpg"))
        file = ('static/' + file_changed)

# We call the inference file, detect.py with the new uploaded file.
        opt = detect.parse_opt(file)
        detect.main(opt)

# The result of the inference will be saved in the directory runs/detect/exp[0..xx]. To get the new file,
# I searched for the last directory created
        latest_subdir_tmp = max(glob.glob('runs/detect/exp*/'), key=os.path.getmtime)
        latest_subdir = latest_subdir_tmp.replace("\\", "/")
        source_file = latest_subdir + file_changed
        #fichero.filename=fichero.filename.replace(".jpeg",".jpg")
        #source_file=latest_subdir+fichero.filename
        #source_file=file

        # And than copy the file, adding ".labeled.jpg" at the end of the name, to differentiate the original file from the labeled one
        dest_file='static/'+fichero.filename+'2.jpg'
        print (source_file,dest_file )
        shutil.copyfile(source_file, dest_file)

# We return the flow to the index.hmtl page, where we are going to show the 2 files, the uploaded and the labeled.
        return render_template('index.html', file_clean = '/static/'+fichero.filename, file_tag=dest_file)

# For the "/" page we only call the index page with 1 picture with and without the label, by default.
@app.route('/')
def upload_form():
    return render_template('index.html',file_clean= '/static/school3.jpg', file_tag='static/school3.jpg2.jpg')



# I execute the webserver on port 9292
if __name__ == '__main__':
	app.run(port=8282)




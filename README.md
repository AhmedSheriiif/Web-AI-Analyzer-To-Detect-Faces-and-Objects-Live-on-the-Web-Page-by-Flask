# Web-AI-Analyzer-Yolo-Emo-Detection-Flask-React
 A web application that uses machine learning models to detect objects and emotions in images and videos uploaded by users. The results are displayed on a dashboard and stored in a database.


<h1><b>Project Overview</b></h1>
<p>This is a web application that uses Flask for the backend and React for the frontend. The application allows users to upload images, videos, or connect to camera through rstp and runs object detection and emotion detection models on them. The detected objects and emotions are stored in a MySQL database managed by XAMPP. The frontend displays the results using graphs and tables.</p>
<h1><b>Technologies Used</b></h1>
<ul>
  <li>Flask: used for building the backend</li>
  <li>React: used for building the frontend</li>
  <li>YOLOv7: used for object detection</li>
  <li>Emotion detection model: used for detecting emotions in images</li>
  <li>XAMPP: used for managing the MySQL database</li>
</ul>
<h1><b>Installation</b></h1>
<ol>
  <li>Clone the repository to your local machine.</li>
  <li>Set up a virtual environment for the project.</li>
  <li>Install the necessary Python packages using pip: <code>pip install -r requirements.txt</code></li>
  <li>Install the appropriate torch version to your pc</li>
  <li>Install Node.js and NPM.</li>
  <li>Start the XAMPP server and create a new database named <code>ai_analysis</code>.</li>
  <li>To create tables and add it to database run cmd and enter the following commands:
  <ul>
   <li><code>python</code>  then press Enter</li>
   <li><code>from app.models import db</code> then press Enter</li>
   <li><code>db.create_all()</code> then press Enter</li>
   <li><code>db.session.commit()</code> then press Enter</li>
   <li><code>exit</code> then press Enter</li>
   </ul>
  </li>
  <li>Run the backend using the following command: <code>python run.py</code>.</li>
</ol>
<h1><b>Usage</b></h1>
<ol>
  <li>Open your browser and navigate to <code>http://localhost:5000</code>.</li>
  <li>Login or register</li>
  <li>Choose one the two models to use: Object Detection using YOLOv7 or Emotion Detection</li>
  <li>Choose one of the three options for uploading content: upload an image, upload a video, or use a camera through rstp.</li>
  <li>Wait for the models to classify the content.</li>
  <li>View the results on the dashboard.</li>
</ol>
<h1><b>Features</b></h1>
<ul>
  <li>Object detection using YOLOv7</li>
  <li>Emotion detection in images</li>
  <li>Live classification of videos and cameras on the web page</li>
  <li>Dashboard with graphs and tables showing the results</li>
  <li>Saving results to a MySQL database managed by XAMPP</li>
</ul>

<h1><b>Contribution</b></h1>
<ul>
  <li>Submit bug reports or feature requests through the Issues tab on GitHub.</li>
  <li>Fork the repository and make changes or additions, then submit a pull request.</li>
</ul>

<h1><b>Contact</b></h1>
<p>If you have any questions or comments about the project, please contact [ahmed.sheriif07@gmail.com].</p>

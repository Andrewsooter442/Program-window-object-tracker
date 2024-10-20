# Program Window object tracker

## Dependency

Python version > 3.10

git
## Installation
On windows open powershell and follow these commands 
```
python -m venv program_window_object_tracker

cd program_window_object_tracker 

.\Scripts\activate

git clone https://github.com/Andrewsooter442/Program-window-object-tracker.git

cd Program-window-object-tracker

Mkdir models

mv .\coco.names .\models\

```
To use a model create a directory inside the models directory with 'model_name' and put the weights file ('model_name'.weights) and the configuration file ('model_name'.cfg) in it (it should look something like this models/model_name/(model_name.weights or model_name.cfg)


For example let's use YOLOv3-tiny

```
mkdir models/YOLOv3-tiny

cd models/YOLOv3-tiny

curl -o YOLOv3-tiny.weights https://pjreddie.com/media/files/yolov3-tiny.weights

"" > "./YOLOv3-tiny.cfg"

```
copy the configuration file from https://github.com/pjreddie/darknet/blob/master/cfg/yolov3-tiny.cfg and past it in the newly created YOLOv3-tiny.cfg

You should be good to run the test model which detects the people on the program and moves the mouse to that position

```


cd ../..

pip install -r .\requirements.txt
```
### To run 
Make sure that the virtual enviroment is active and navigate inside the Program-window-object-tracker directory and run the gui.py

`python gui.py`

#include "Vision.h"

Vision::Vision(string path, stream_type type, int cameraID){
	_path = path,
	_type = type,
	_cameraID = cameraID;

}

void Vision::load() {

}

void Vision::stream() {
	int delay = 0;
	switch(_type){
	
	case stream_type::VIDEO:
	{
		delay = 1;
		VideoCapture vid(_path);
		while (true) {
			vid.read(_stream);
			imshow("Video", _stream);
			waitKey(delay);
		}
		break;
	}


	case stream_type::CAMERA:
	{
		delay = 1;
		VideoCapture cam(_cameraID);
		while (true) {
			cam.read(_stream);
			imshow("Cam_Stream", _stream);
			waitKey(delay);
		}
		break;
	}

	case stream_type::IMAGE:
		delay = 0;
		_stream = imread(_path);
		if (!_stream.empty()) {
			imshow("Image", _stream);
			waitKey(delay);
		}

		else {
			cout << "ERROR: IMAGE NOT FOUND" << endl;
		}
		break;


	default:
		cout << "ERROR: NO STREAM FORMAT FOUND" << endl;
	break;
	}

}

void Vision::colour_detector() {

}

void Vision::edge_detector() {

}
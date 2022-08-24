#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#pragma once

using namespace std;
using namespace cv;

enum stream_type{ IMAGE, VIDEO, CAMERA };
class Vision {
public:
	Vision(string path, stream_type type, int cameraID);

private:
	string _path;
	stream_type _type;
	Mat _stream;
	int _cameraID;

public:
	string get_path() { return _path; }
	stream_type get_type() { return _type; }
	int get_cameraID() { return _cameraID; }
	void set_path(string new_path) { _path = new_path; }
	void set_type(stream_type new_type) { _type = new_type; }
	void set_cameraID(int newID) { _cameraID = newID; }

	void load();
	void stream();
	void colour_detector();
	void edge_detector();

	
};
#include "Vision.h"

int main() {
	string path = "";
	stream_type stream = stream_type::CAMERA;
	int cameraID = 0;
	Vision vision_obj = Vision(path, stream, cameraID);
	vision_obj.stream();
	return 0;
}
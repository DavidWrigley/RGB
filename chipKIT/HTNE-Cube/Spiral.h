#include "WProgram.h"
#include "Animation.h"

#ifndef _SPIRAL_
#define _SPIRAL_

class Spiral : public Animation{
	public:
		Spiral();
		uint8_t animate(Cube &c);
	protected:
};

#endif
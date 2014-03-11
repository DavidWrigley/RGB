#include "WProgram.h"
#include "Animation.h"

#ifndef _RANDOM_FLICKER_
#define _RANDOM_FLICKER_


class RandomFlicker : public Animation{
	public:
		RandomFlicker();
		uint8_t animate(Cube &c);
	protected:
		int8_t rainDrops;
		int8_t rX, rY, rZ;
};

#endif
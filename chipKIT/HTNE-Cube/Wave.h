#include "WProgram.h"
#include "Animation.h"

#ifndef wave_h
#define wave_h
class Wave : public Animation{
	public:
		Wave();
		uint8_t animate(Cube &c);
	protected:
};
#endif

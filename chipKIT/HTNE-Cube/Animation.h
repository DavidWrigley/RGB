#include "Wprogram.h"
#include "Cube.h"

#ifndef _ANIMATION_
#define _ANIMATION_

class Animation{
	public:
		Animation();
		virtual ~Animation();
		virtual uint8_t animate(Cube &c);
		void setTempCubeColour(uint8_t x, uint8_t y, uint8_t z, uint32_t col);
		void ORTempCubeColour(uint8_t x, uint8_t y, uint8_t z, uint32_t col);
		uint32_t getTempCubeColour(uint8_t x, uint8_t y, uint8_t z);
		void addPhase(double val);
		void addColourPoint(uint8_t val);
		void bouncePos(void);
		void clearAllAnimations(void);
		void clearTempCubeArray(void);
		void copyTempCubeArray(Cube &c);
		void copyTempCubeArrayWithException(Cube &c, uint32_t ex);
		void colour2DRect(uint8_t axis, uint8_t pos, uint32_t val);
		double mapd(double in, double inMin, double inMax, double outMin, double outMax);
	protected:
		int16_t dir;
		int16_t pos;
		uint16_t slow;
		uint16_t colourPoint;
		uint32_t tempCubeColourArray[Vd];
		uint32_t count;
		double X, Y, Z;
		double phase;
};

#endif
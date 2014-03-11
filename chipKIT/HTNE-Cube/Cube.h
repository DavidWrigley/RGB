#include "WProgram.h"
#include <math.h>
#include <stdlib.h>
#include <sys/attribs.h>

#ifndef cube_h
#define cube_h

#define PI  3.14159265358979323846
#define Xd 8
#define Yd 8
#define Zd 8
#define Vd Xd*Yd*Zd
#define maxBAMbit 8						//resolution of the modulation
#define maxBitColour 255				//max colour size must be (2^maxBAMbit - 1)
#define colourWheelLength 255			//length of the colour wheel, this length makes a very smooth colour wheel
#define CUBE_ENABLE LATDCLR = 0x0001	
#define CUBE_DISABLE LATDSET = 0x0001

class Cube{
	public:
		Cube();
		void init(void);
		void fillColourWheel(void);
		uint32_t getColourFromWheel(uint8_t pos);
		void layer(uint8_t z, uint8_t bit_pos);
		void latch(void);
		void ORcubeVoxel(uint8_t x, uint8_t y, uint8_t z, uint32_t input);
		void fill(uint32_t val);
		void clearCube(void);
		uint8_t getRow(uint8_t z);
		uint32_t cubeColourArray[Xd][Yd][Zd];
	protected:
		uint32_t CLK, LE, SDIR, SDIG, SDIB, OE;
		volatile uint8_t ROW[Zd];
		uint32_t colourWheel[colourWheelLength];
};

#endif

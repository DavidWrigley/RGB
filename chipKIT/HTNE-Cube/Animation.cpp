#include "Animation.h"

//Constructor set all the values to default
Animation::Animation(){
	X = 0; Y = 0; Z = 0;
	count = 0;
	phase = 0;
	dir = 1;
	pos = 0;
	slow = 0;
	colourPoint = 0;
	clearTempCubeArray();
}

//destructor, just delete the large array
Animation::~Animation(){
	delete[] tempCubeColourArray;
}

//virtual animation does nothing
uint8_t Animation::animate(Cube &c){
	return 1;
}

//Set the colour at position X, Y, Z in the linear array
void Animation::setTempCubeColour(uint8_t x, uint8_t y, uint8_t z, uint32_t col){
	tempCubeColourArray[(Xd*Yd)*z + (Yd)*y + x] = col;
}

//OR the colour at position X, Y, Z with the input colour
void Animation::ORTempCubeColour(uint8_t x, uint8_t y, uint8_t z, uint32_t col){
	tempCubeColourArray[(Xd*Yd)*z + (Yd)*y + x] |= col;
}

//return the value of the colour at the position X, Y, Z
uint32_t Animation::getTempCubeColour(uint8_t x, uint8_t y, uint8_t z){
	uint32_t colour;
	colour = tempCubeColourArray[(Xd*Yd)*z + (Yd)*y + x];
	return colour;
}

//Add number to phase, loop back to 0 if phase exceeds 2PI
void Animation::addPhase(double val){
	phase += val;
	while(phase >= 2*PI){
		phase -= 2*PI;
	}
}

//add number to colour wheel pointer, loop pack to zero if pointer exceeds wheel length
void Animation::addColourPoint(uint8_t val){
	colourPoint += val;
	while(colourPoint >= colourWheelLength){
		colourPoint -= colourWheelLength;
	}
}

//bounce the pos variable between 0 and 7
void Animation::bouncePos(void){
	pos += dir;
	
	if(pos >= Zd){
		dir *= -1;
		pos = Zd-1;
	}
	if(pos < 0){
		dir *= -1;
		pos = 0;
	}
}

//set all values to default
void Animation::clearAllAnimations(void){
	X = 0; Y = 0; Z = 0;
	phase = 0;
	dir = 1;
	pos = 0;
	slow = 0;
	colourPoint = 0;
	clearTempCubeArray();
}

//clear the dummy array
void Animation::clearTempCubeArray(void){
	memset(tempCubeColourArray, 0 , Vd*sizeof(uint32_t));
}

//copy dummy array into working cube array
void Animation::copyTempCubeArray(Cube &c){
	for(uint8_t x = 0; x < Xd; x++){
		for(uint8_t y = 0; y < Yd; y++){
			for(uint8_t z = 0; z < Zd; z++){
				c.cubeColourArray[x][y][z] = getTempCubeColour(x, y, z);
			}
		}
	}
}

//copy the dummy array into working cube array BUT skip a colour 
//usefull if you need to set a value in the array for memory purposes 
void Animation::copyTempCubeArrayWithException(Cube &c, uint32_t ex){
	uint32_t check = 0;
	for(uint8_t x = 0; x < Xd; x++){
		for(uint8_t y = 0; y < Yd; y++){
			for(uint8_t z = 0; z < Zd; z++){
				check = getTempCubeColour(x, y, z);
				if(check != ex){
					c.cubeColourArray[x][y][z] = check;
				}else{
					c.cubeColourArray[x][y][z] = 0;
				}
			}
		}
	}
}

//fill one 2D panel in the chosen axis at posi
void Animation::colour2DRect(uint8_t axis, uint8_t posi, uint32_t val){
	switch(axis){
		case 'X':
			for(uint8_t y = 0; y < Yd; y++){
				for(uint8_t z = 0; z < Zd; z++){
					ORTempCubeColour(posi, y, z, val);
				}
			}
			break;
		case 'Y':
			for(uint8_t x = 0; x < Xd; x++){
				for(uint8_t z = 0; z < Zd; z++){
					ORTempCubeColour(x, posi, z, val);
				}
			}
			break;
		case 'Z':
			for(uint8_t x = 0; x < Yd; x++){
				for(uint8_t y = 0; y < Yd; y++){
					ORTempCubeColour(x, y, posi, val);
				}
			}
			break;
	}
}

//map a number to a new range
double Animation::mapd(double in, double inMin, double inMax, double outMin, double outMax){
    double out;
    out = (in-inMin)/(inMax-inMin)*(outMax-outMin) + outMin;
    return out;
}
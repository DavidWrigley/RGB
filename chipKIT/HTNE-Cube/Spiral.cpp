#include "Spiral.h"

Spiral::Spiral(){
}

uint8_t Spiral::animate(Cube &c){
	//effectively slow the animation by skipping it
	slow++;
	if(slow < 1){
		return 0;
	}
	slow = 0;

	clearTempCubeArray();
	
	for(uint8_t z = 0; z < Zd; z++){
		for(uint8_t i = 0; i < 3; i++){
			Y = cos(phase + mapd(z, 0, Zd-1, 0, 2*PI) + i*PI/8);
			X = sin(phase + mapd(z, 0, Zd-1, 0, 2*PI) + i*PI/8);
			Y = mapd(Y, -1.1, 0.9, 0, Yd-1);
			X = mapd(X, -1.1, 0.9, 0, Xd-1);
			setTempCubeColour((uint8_t)X, (uint8_t)Y, z, c.getColourFromWheel(colourPoint+10*z));
		}
	}
	
	addColourPoint(1);
	addPhase(PI/10);
	
	copyTempCubeArray(c);

	return 1;
}


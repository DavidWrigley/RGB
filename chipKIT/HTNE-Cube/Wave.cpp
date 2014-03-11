#include "Wave.h"

Wave::Wave(){
}

uint8_t Wave::animate(Cube &c){
	//effectively slow the animation by skipping it
    slow++;
    if(slow < 1){
		return 0;
    }
    slow = 0;
    
    clearTempCubeArray();
    
    X = 0;
    Y = 0;
    Z = 0;

    for(uint8_t x = 0; x < Xd; x++){
		for(uint8_t y = 0; y < Yd; y++){
			X = cos(phase + mapd(x,0,Xd-1,0,2*PI));
			Y = cos(phase + PI/32 + mapd(y,0,Yd-1,0,2*PI));
			Z = X + Y;
			Z = round(mapd(Z,-2,2,0,Zd-1));
			setTempCubeColour(x, y,(uint8_t)Z, c.getColourFromWheel(colourPoint + x*2 + y*4 + Z*6));
		}
    }
	
	addColourPoint(1);
    addPhase(PI/16);
	
    copyTempCubeArray(c);

    return 1;
}

#include "RandomFlicker.h"

RandomFlicker::RandomFlicker(){
	rainDrops = 0;
	rX = 0;
	rY = 0;
	rZ = 0;
}

uint8_t RandomFlicker::animate(Cube &c){
	//effectively slow the animation by skipping it
	slow++;
    if(slow < 2){
		return 0;
    }
	slow = 0;
	
	for(uint8_t x = 0; x < Xd; x++){
		for(uint8_t y = 0; y < Yd; y++){
			for(int8_t z = Zd-1; z > 0; z--){
				setTempCubeColour(x, y, z, getTempCubeColour(x, y, z-1));
				setTempCubeColour(x, y, z-1, 0);
				if(getTempCubeColour(x, y, z-1) != 0){
					if(z < 7){
						setTempCubeColour(x, y, 0, 0xFFFFFF);
					}
				}
			}
		}
	}
	
	for(uint8_t i = 0; i < 10; i++){
		if(rainDrops > rand()%16+0){
			rX = rand()%8+0;
			rY = rand()%8+0;
			while(getTempCubeColour(rX, rY, 0) != 0 && count < 100){
				rX = rand()%8+0;
				rY = rand()%8+0;
				count++;
			}
			setTempCubeColour(rX, rY, 0, c.getColourFromWheel(rand()&254+0));
			rainDrops = 0;
		}
	}
	count = 0;
	
	copyTempCubeArrayWithException(c, 0xFFFFFF);
    rainDrops++;
	
	return 1;
}
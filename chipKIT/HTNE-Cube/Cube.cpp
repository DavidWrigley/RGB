#include "Cube.h"

Cube::Cube(){
	LE = 0x00002; //5, D1
	CLK = 0x0004; //6, D2
	SDIR = 0x00008; //7, D9
	SDIG = 0x0400; //8, D10
	SDIB = 0x0200; //9, D3
	OE = 0x0001; //3, D0
	//ROW = {0x40, 0x10, 0x20}; //38-F6,39-F4,40-F5
	ROW = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80};//26, 27, 28, 29, 30, 31, 32, 33, E0-7
	clearCube();
}

void Cube::init(void){
	//digital IOs
	//setup PORTD
	TRISDCLR = CLK|LE|SDIR|SDIG|SDIB|OE;
	LATDCLR = CLK|LE|SDIR|SDIG|SDIB|OE;
	
	//setup PORTE
	for(uint8_t i = 0; i < Zd; i++){
		TRISECLR = ROW[i];
		LATESET = ROW[i];
	}
	
	clearCube();
	fillColourWheel();
	
	//timer 
	T2CON = 0x0;        //1:1 prescale
	TMR2 = 0x0;         //clear timer reg
	PR2 = 0x0150;       //load period reg 

	INTCONSET = 0x00001000;  //multi vector mode
	IPC2SET = 0x0000001F;    //T2 highest priority
	IFS0CLR = 0x00000100;    //clear T2 interrupt flag
	IEC0SET = 0x00000100;    //enable T2 interrupt
	T2CONSET = 0x8000;     //start T2
  
	asm volatile("ei");    //enable interrupt
}

//create a smooth vector array of colours by moving in a circle about the colour wheel 
void Cube::fillColourWheel(void){
	float red = 0;
	float green = 0;
	float blue = 0;
	uint16_t phase = 0;
	
	while(phase < colourWheelLength/3){
		//round the colour wheel
		//red up, green 0, blue down
		red = maxBitColour*sin(PI*phase/(2*colourWheelLength/3));
		green = 0;
		blue = maxBitColour*cos(PI*phase/(2*colourWheelLength/3));
		colourWheel[phase] = ((uint8_t)red)|((uint8_t)green<<8)|((uint8_t)blue<<16);
		phase++;
	}
	
	
	while(phase < 2*colourWheelLength/3){
		//round the colour wheel 
		//red down, green up, blue 0
		red = maxBitColour*cos(PI*(phase-colourWheelLength/3)/(2*colourWheelLength/3));
		green = maxBitColour*sin(PI*(phase-colourWheelLength/3)/(2*colourWheelLength/3));
		blue = 0;
		colourWheel[phase] = ((uint8_t)red)|((uint8_t)green<<8)|((uint8_t)blue<<16);
		phase++;
	}
	
	while(phase < colourWheelLength){
		//round the colour wheel
		//red 0, green down, blue up
		red = 0;
		green = maxBitColour*cos(PI*(phase-2*colourWheelLength/3)/(2*colourWheelLength/3));
		blue = maxBitColour*sin(PI*(phase-2*colourWheelLength/3)/(2*colourWheelLength/3));
		colourWheel[phase] = ((uint8_t)red)|((uint8_t)green<<8)|((uint8_t)blue<<16);
		phase++;
	}
}

//retrieve a colour from the colour wheel
uint32_t Cube::getColourFromWheel(uint8_t pos){
	uint32_t val = 0;
	
	//make position is not larger than the length of the array
	while(pos >= colourWheelLength){
		pos -= colourWheelLength;
	}
	
	val = colourWheel[pos];
	return val;
}

//used in the interrupt
//for the given z and BAM bit_pos it send the layer data to the LED drivers
//multiplexing and BAM rolled into one
void Cube::layer(uint8_t z, uint8_t bit_pos){
	uint32_t on = 0;
  
	for(int8_t y = 0; y < Yd; y++){
		for(int8_t x = 0; x < Xd; x++){
			on = 0;
			if((cubeColourArray[x][y][z]>>16)&(0x01<<bit_pos)){
				on |= SDIR;
			}
			if((cubeColourArray[x][y][z]>>8)&(0x01<<bit_pos)){
				on |= SDIG;
			}
			if((cubeColourArray[x][y][z])&(0x01<<bit_pos)){
				on |= SDIB;
			}
			
			//clock in the data to the three parallel data lines at the same time
			LATDSET = on;
			LATDSET = CLK;
			LATDCLR = CLK|SDIR|SDIG|SDIB;
		}
	}
	latch();
}

//latch the LED drivers to display the currently loaded layer
void Cube::latch(void){
  LATDSET = LE;
  LATDCLR = LE;
}

//get the current working row
uint8_t Cube::getRow(uint8_t z){
	return ROW[z];
}

//OR the input with the value already in the cube at the position (x, y, z)
void Cube::ORcubeVoxel(uint8_t x, uint8_t y, uint8_t z, uint32_t input){
	cubeColourArray[x][y][z] |= input;
}

//fill the cube with an input colour
void Cube::fill(uint32_t val){
	for(int8_t z = 0; z < Zd; z++){
		for(int8_t y = 0; y < Yd; y++){
			for(int8_t x = 0; x < Xd; x++){
				cubeColourArray[x][y][z] = val;
			} 
		}
	}
}

//clear the cube array and the cube
void Cube::clearCube(void){
	memset(cubeColourArray, 0, Vd*sizeof(uint32_t)); 
	layer(0,0);
	latch();
}




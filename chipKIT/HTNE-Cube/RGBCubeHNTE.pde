////////////////////////////////////////////////////////////////////////////////////
//Feel free to use or edit this code how you like.                                //
//I put a lot of time and effort into this code so please spread                  //
//the love by referencing me and my site if you use this in your own projects     //
//                                                                                //
//Cheers                                                                          //
//Nick Schulze                                                                    //
//www.HowNotToEngineer.com                                                        //
///////////////////////////////////////////////////////////////////////////////////

#include "Cube.h"
#include "Wave.h"
#include "Spiral.h"
#include "RandomFlicker.h"

#define ANIMATION_NUMBER 3

//CLASSES
//cube and serial are stored on the stack because they never get deleted
Cube rgb;   

//the rest of the animations are kept on the heap for dynamic memory allocation  
Animation *wave;
Animation *spiral;
Animation *randomFlicker;

//VARIABLES
uint8_t frame_done_count = 0;		
uint32_t change_anim_count = 0;
uint8_t animation_change = 2;		//set this value to choose the initial animation
uint8_t choose_animation = 0;

//MAIN FUNCTION
int main(void){
	rgb.init();    	//initialise the timers and interrupts
	
	//create the initial animation
	doChangeAnimation();
	
	//ANIMATE LOOP
	//Animations get data from the port or fill the cube array with the next frame
	for(;;){
		//delete current animation and create new animation
		if(animation_change != 0){
			doChangeAnimation();
			change_anim_count = 0;
		}
		
		//load at least two frames before animating next frame
		//unless receiving serial data
		if(frame_done_count > 2 || choose_animation == 1){
			//switch between the different on board animations
			switch(choose_animation){
				case 1:
					//sorry no serial input in the free version ;)
					break;
				case 2:
					wave->animate(rgb);
					break;
				case 3:
					spiral->animate(rgb);
					break;
				case 4:
					randomFlicker->animate(rgb);
					break;
			}

			frame_done_count = 0;
		}
	}

	return 0;
}

//Dynamic memory allocation
//when animation change is set to a value other than 0 this
//function will delete the current animation and create the new animation
void doChangeAnimation(void){
	//delete the currently running animation
	switch(choose_animation){
		case 1:
			//serial animation is on stack, don't delete
			break;
		case 2:
			delete wave;
			break;
		case 3:
			delete spiral;
			break;
		case 4:
			delete randomFlicker;
			break;
	}
	
	//swap the variables over
	choose_animation = animation_change;
	animation_change = 0;
	
	//create an instance of the new animation
	switch(choose_animation){
		case 1:
			//serial always on the stack don't create
			break;
		case 2:
			wave = new Wave;
			break;
		case 3:
			spiral = new Spiral;
			break;
		case 4:
			randomFlicker = new RandomFlicker;
			break;
	}
}

//INTERRUPT
//The interrupt handles the Bit Angle Modulation and 
#ifdef __cplusplus
extern "C" {
#endif

//variables used only in the BAM function
int32_t bit_count = 0x00;
int32_t bit_pos = 0x00;
int32_t bit_length = 0x01;
int16_t z = 0;

void __ISR(_TIMER_2_VECTOR, ipl7) TimerHandler(void){
	//change to next animation, or switch back to onboard animations if serial data not being recieved
	if(change_anim_count > 2000 || (choose_animation == 1 && change_anim_count > 50)){
		if(choose_animation == 1){
			animation_change = 2;
		}else{
			animation_change = choose_animation+1;
		}
		if(animation_change > ANIMATION_NUMBER + 1){
			animation_change = 2;
		}
		change_anim_count = 0;
	}
	
	//Bit Angle Modulation
	//only load in data once for every bit in the BAM
	if(bit_count == 0){
		CUBE_DISABLE;				//disable the output while loading in data, fixed some flickering issues
		rgb.layer(z, bit_pos);		//send data to the cube
		LATECLR = rgb.getRow(z);	//turn on the new row transistor
		CUBE_ENABLE;				//enable the output
	}
    
	//increment the bit counter 
	bit_count+=0x01;
	
	//increment the actual bit position and increase the length of the next delay
	if(bit_count >= bit_length){
		bit_pos += 0x01;
		bit_length = bit_length<<0x01;
		bit_count = 0x00;
	}
  
	//turn off the current row and switch to the next row
  	if(bit_pos >= maxBAMbit){
		bit_pos = 0x00;
		bit_count = 0x00;
		bit_length = 0x01;
		LATESET = rgb.getRow(z);
		z++;
		if (z > Zd-1){
			z = 0; 
			frame_done_count++;
			change_anim_count++;
		}
	}
  
	IFS0CLR = 0x00000100;  //reset interrupt flag
}

#ifdef __cplusplus
}
#endif

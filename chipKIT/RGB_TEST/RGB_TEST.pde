/**
 * LIBS
 */
#include <time.h>
#include <plib.h>
#include <Wiring.h>
#include <chipKITEthernet.h>

/**
 * Local LIBS
 */
#include "pin_out.h"

 /**
  * Defines
  */
#define layermax 8
#define pixelmax 64
#define redmax 8
#define greenmax 8
#define bluemax 8

/**
 * Global Varables
 */
// Ethernet 
// byte ip[] = { 192,168,1,190 };
byte mac[] = { 0x01, 0x23, 0x45, 0x67, 0x8A, 0xBC };
byte gateway[] = { 192,168,1, 1 };
byte subnet[] = { 255, 255, 255, 0 };
// local port to listen on
unsigned short localPort = 8888;
// start TCP server
Server server = Server(8888);
// ProcessString Varables
int bytes_read = 0;
int currentDataPossition = 0;
// BAM varables
int colourcounter = 0;
int duty = 8;
// 64 bit mask
uint64_t Mask = 0xFFFFFFFFFFFFFFFF;
// 64 bit shift
uint64_t shift = 1;
// port F Register
uint32_t on = 0;
// SPI values when performing BAM
uint64_t spiRed = 0;
uint64_t spiGreen = 0;
uint64_t spiBlue = 0;
// SPI data being processed by SPISend()
uint64_t dataRed = 0;
uint64_t dataGreen = 0;
uint64_t dataBlue = 0;
// Perform colour changed, Testing
char direction = 1;
char redchange = 0;
char bluechange = 0;
char greenchange = 0;
// 8 layers, 64 pixels, 3 colours
char ledArray[8][64][3];
// layer arrays
char layerPossitionCounter = 0;
char layerArray[8] = { layerpin_1, layerpin_2, layerpin_3, layerpin_4, 
                       layerpun_5, layerpin_6, layerpin_7, layerpin_8};
//pixeltest
char pixelteston = 1;
char currenttestlayer = 0;
char currenttestpixel = 0;
char testredpixel = 1;
char testgreenpixel = 0;
char testbluepixel = 0;
// buffer
char fromclient[2570];
// read varables
uint8_t readLayer = 0;
uint8_t readPixel = 0;
uint8_t readRed = 0;
uint8_t readGreen = 0;
uint8_t readBlue = 0;

void setup() {

    Serial.begin(9600); 
    Serial.println("Initilising");

    Serial.println("Ethernet");
    // start the Ethernet and UDP:
    // Ethernet.begin(mac,ip,gateway,subnet);
    Ethernet.begin();  // use DHCP

    server.begin();

    Serial.println("SPI");

    // set pins to output
    TRISECLR = pinSS|pinSCK|pinMOSIR|pinMOSIG|pinMOSIB|pinOE;

    // clear OE, making the SPI chip output.
    LATECLR = pinOE;

    Serial.println("Layers");

	// driver pins
	pinMode(layerArray[0], OUTPUT);
	pinMode(layerArray[1], OUTPUT);
	pinMode(layerArray[2], OUTPUT);
	pinMode(layerArray[3], OUTPUT);
	pinMode(layerArray[4], OUTPUT);
	pinMode(layerArray[5], OUTPUT);
	pinMode(layerArray[6], OUTPUT);
	pinMode(layerArray[7], OUTPUT);

    digitalWrite(layerArray[0], 1);
    digitalWrite(layerArray[1], 1);
    digitalWrite(layerArray[2], 1);
    digitalWrite(layerArray[3], 1);
    digitalWrite(layerArray[4], 1);
    digitalWrite(layerArray[5], 1);
    digitalWrite(layerArray[6], 1);
    digitalWrite(layerArray[7], 1);

    Serial.println("Timers");

    // ledarray modifier
    OpenTimer3(T3_ON | T3_PS_1_256 | T3_SOURCE_INT, 50000);

    // Set up the timer interrupt with a priority of 2
    INTEnable(INT_T3, INT_ENABLED);
    INTSetVectorPriority(INT_TIMER_3_VECTOR, INT_PRIORITY_LEVEL_2);
    INTSetVectorSubPriority(INT_TIMER_3_VECTOR, INT_SUB_PRIORITY_LEVEL_0);

    // Enable multi-vector interrupts
    INTConfigureSystem(INT_SYSTEM_CONFIG_MULT_VECTOR);
    INTEnableInterrupts();

    // can only have 2 attatched timers
    attachCoreTimerService(bamCallback);
    attachCoreTimerService(layerCallback);
    
    Serial.println("Zeroing!");

    for(int i = 0; i < 8; i++) {
        for(int j = 0; j < 64; j++) {
            for(int k = 0; k < 3; k++) {
                ledArray[i][j][k] = 0;
            }
        }
    }
    
    Serial.println("Finished!");
}

void loop() {

    // if there's data available, read a packet
    Client client = server.available();

    if(client == true) {

        bytes_read = client.read((uint8_t*)fromclient,2560);
        currentDataPossition = 0; 

        Serial.print("Bytes_Read: ");
        Serial.print(bytes_read,DEC);
        Serial.println(""); 

        for(int i = 0; i < bytes_read; i += 5) {
            // define the packet [] is 1 byte 0 -> 256
            // [Layer][Pixel][Red][Green][Blue]#
            // read the data from the ethernet stream
            readLayer = fromclient[i];
            readPixel = fromclient[i+1];
            readRed = fromclient[i+2];
            readGreen = fromclient[i+3];
            readBlue = fromclient[i+4];

            // assign the colour read and also check for safty
            if( ((bytes_read % 5) == 0)
                &&((readLayer < 8)&&(readLayer >= 0))
                &&((readPixel < 64)&&(readPixel >= 0))
                &&((readRed <= 8)&&(readRed >= 0))
                &&((readGreen <= 8)&&(readGreen >= 0))
                &&((readBlue <= 8)&&(readBlue >= 0)) ) {
                ledArray[readLayer][readPixel][0] = readRed;
                ledArray[readLayer][readPixel][1] = readGreen;
                ledArray[readLayer][readPixel][2] = readBlue;
            } else {
                // ignore it
                // Serial.println("Bad");
            }
            
/*
            Serial.print("i: ");
            Serial.print(i,DEC);
            Serial.print(" RL: ");
            Serial.print(readLayer,DEC);
            Serial.print(" RP: ");
            Serial.print(readPixel,DEC);
            Serial.print(" R: ");
            Serial.print(readRed,DEC);
            Serial.print(" G: ");
            Serial.print(readGreen,DEC);
            Serial.print(" B: ");
            Serial.print(readBlue,DEC);
            Serial.println("");
*/
        }
    }
}

/**
 * Custom SPI function to send 3 lines of data simultaniously
 * @param dataRed   The Value of the RED registers
 * @param dataGreen The Value of the GREEN registers
 * @param dataBlue  The Value of the BLUE registers
 */
void SpiSend(uint64_t dataRed, uint64_t dataGreen, uint64_t dataBlue) {

    // start communication
    LATECLR = pinSS;

    // for the number of bytes, send through
    for(int i = 0; i < 64; i++) {

        on = 0;

        // clock off
        LATECLR = pinSCK;

        // check the data for Red
        if((1 & dataRed) == 1) {
            on = (on | pinMOSIR);
        } 

        //  Green
        if((1 & dataGreen) == 1) {
            on = (on | pinMOSIG);
        } 

        // Blue
        if((1 & dataBlue) == 1) {
            on = (on | pinMOSIB);
        } 

        // shift down to the next set of data
        dataRed = (dataRed >> 1);
        dataGreen = (dataGreen >> 1);
        dataBlue = (dataBlue >> 1);

        // set the data
        LATESET = on;
        // clock the data
        LATESET = pinSCK;
        // clear the MOSI pins
        LATECLR = on;
    }
    
    // shift the register into device
    LATESET = pinSS;

    // reset SPI Communication
    LATECLR = (pinSS|pinMOSIR|pinMOSIG|pinMOSIB|pinSCK);
}

/**
 * Bit Angle Manipulation callback, this deals with the intensity of the colour
 * being produced by the LED's, 8 is full, 0 is off
 * @param  currentTime Unknown
 * @return             Current time + when you want it to go off next
 */
uint32_t bamCallback(uint32_t currentTime) {

    // look into the colour array and determin for how long to hold the pins high
    // iterate over the layer checking colours and adjust.
    for(int i = 0; i < 64; i++) {

        shift = 1;
        Mask = 0xFFFFFFFFFFFFFFFF;
        if(colourcounter < ledArray[layerPossitionCounter-1][i][0]) {
            // meaning the pixel should be on
            spiRed = (spiRed | (shift << i));
        } else {
            // XOR the mask, making it 0 (in the correct spot)
            shift = (shift << i);
            Mask = (Mask ^ shift);
            spiRed = (spiRed & Mask);
        }

        shift = 1;
        Mask = 0xFFFFFFFFFFFFFFFF;
        if(colourcounter < ledArray[layerPossitionCounter-1][i][1]) {
            spiGreen = (spiGreen | (shift << i));
        } else {
            shift = (shift << i);
            Mask = (Mask ^ shift);
            spiGreen = (spiGreen & Mask);
        }

        shift = 1;
        Mask = 0xFFFFFFFFFFFFFFFF;
        if(colourcounter < ledArray[layerPossitionCounter-1][i][2]) {
            spiBlue = (spiBlue | (shift << i));
        } else {
            shift = (shift << i);
            Mask = (Mask ^ shift);
            spiBlue = (spiBlue & Mask);
        }
    }

    //LATESET = pinOE;

    // send the colours
    SpiSend(spiRed, spiGreen, spiBlue);

    //LATECLR = pinOE;
    
    // reset the colours
    spiRed = 0;
    spiBlue = 0;
    spiGreen = 0;

    // increment the colourcounter
    if(colourcounter > duty) {
        // do nothing
    } else {
        colourcounter++;
    }
    //interrupts();
    return (currentTime + CORE_TICK_RATE*.2);
    // return (currentTime + CORE_TICK_RATE*200);
}

/**
 * Layer callback, when the layers need to switch, this had to be
 * in time with the BAM or the colours will not look the same for
 * each layer, this needs further testing
 * @param  currentTime Unknown
 * @return             dito from above
 */
uint32_t layerCallback(uint32_t currentTime) {

    // TODO: replace this with direct access to the pins, not using digital write
    // also the mosfet will operate the other way, meaning. when the layer is low
    // the mosfet will be active, need to slow down all the timers and observe.

    if(layerPossitionCounter == 8) {
        layerPossitionCounter = 0;
    }

    spiRed = 0;
    spiGreen = 0; 
    spiBlue = 0;
    // force the colour high, as it may still be low from last layer
    SpiSend(0x0000000000000000,0x0000000000000000,0x0000000000000000);
    // LATESET = pinOE;
    // SpiSend(0xFFFFFFFFFFFFFFFF,0xFFFFFFFFFFFFFFFF,0xFFFFFFFFFFFFFFFF);

    // turn off the last layer
    if(layerPossitionCounter == 0) {
        digitalWrite(layerArray[7], 1);
    } else {
        digitalWrite(layerArray[(layerPossitionCounter - 1)], 1);
    }

    // eneable the next layer
    digitalWrite(layerArray[layerPossitionCounter], 0);
    // LATECLR = pinOE;

    /* HOME TEST
    // turn off the last layer HOME TEST
    if(layerPossitionCounter == 0) {
        digitalWrite(layerArray[7], 0);
    } else {
        digitalWrite(layerArray[(layerPossitionCounter - 1)], 0);
    }

    // eneable the next layer
    digitalWrite(layerArray[layerPossitionCounter], 1);
    */

    // reset the BAM counter
    colourcounter = 0;

    // increment
    layerPossitionCounter++;       
    return (currentTime + CORE_TICK_RATE*1.6);
    // return (currentTime + CORE_TICK_RATE*1600);
}

extern "C"
{
    void __ISR(_TIMER_3_VECTOR,ipl2) playSa(void)
    {    
        if(pixelteston == 1) {
            // if red test is on, set the red pixel
            if(testredpixel == 1) {
                ledArray[currenttestlayer][currenttestpixel][0] = 8;
            }
            // if green test is on, set the green pixel
            if(testgreenpixel == 1) {
                ledArray[currenttestlayer][currenttestpixel][1] = 8;
            }
            // if blue test is on, set the blue pixel
            if(testbluepixel == 1) {
                ledArray[currenttestlayer][currenttestpixel][2] = 8;
            }
            // if the currentpixel is at its max, 63, reset it to 0 and switch layer
            if(currenttestpixel == 63) {
                // increment the layer
                currenttestlayer += 1;
                // set the current pixel back to zero
                currenttestpixel = 0;
            }
            // check the layer is not past its maximum of 8 if it is, set it back to zero
            if(currenttestlayer == 8) {
                currenttestlayer = 0;
            }
        }
        INTClearFlag(INT_T3);
    }
} 

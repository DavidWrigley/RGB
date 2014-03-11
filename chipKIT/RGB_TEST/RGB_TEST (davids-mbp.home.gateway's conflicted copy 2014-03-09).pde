#include <time.h>
#include <plib.h>
#include <Wiring.h>
#include <chipKITEthernet.h>

#include "pin_out.h"

// Ethernet 
// byte ip[] = { 192,168,1,190 };
byte mac[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
byte gateway[] = { 192,168,1, 1 };
byte subnet[] = { 255, 255, 255, 0 };

// local port to listen on
unsigned short localPort = 8888;

// start TCP server
Server server = Server(8888);

int bytes_read = 0;
int currentDataPossition = 0;

// Globals

int colour = 78;
int prevcolour = 78;

int brightness = 27;
int colourcounter = 0;
int duty = 8;

// 64 bit mask
uint64_t Mask = 0xFFFFFFFFFFFFFFFF;
// 64 bit shift
uint64_t shift = 1;

uint32_t on = 0;

uint64_t spiRed = 0;
uint64_t spiGreen = 0;
uint64_t spiBlue = 0;

uint64_t dataRed = 0;
uint64_t dataGreen = 0;
uint64_t dataBlue = 0;

char incomingByte = 0;
char direction = 1;

char redchange = 0;
char bluechange = 0;
char greenchange = 0;

// 8 layers, 64 pixels, 3 colours
char ledArray[8][64][3];
String myString;

// layer arrays
char layerPossitionCounter = 0;
char layerArray[8] = { layerpin_1, layerpin_2, layerpin_3, layerpin_4, 
                       layerpun_5, layerpin_6, layerpin_7, layerpin_8};

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
    TRISECLR = pinSS|pinSCK|pinMOSIR|pinMOSIG|pinMOSIB;

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

    Serial.println("Timers");

    // ledarray modifier
    OpenTimer3(T3_ON | T3_PS_1_256 | T3_SOURCE_INT, 50000);

    // Set up the timer interrupt with a priority of 2
    INTEnable(INT_T3, INT_ENABLED);
    INTSetVectorPriority(INT_TIMER_3_VECTOR, INT_PRIORITY_LEVEL_2);
    INTSetVectorSubPriority(INT_TIMER_3_VECTOR, INT_SUB_PRIORITY_LEVEL_0);

    //delay(1);

    // Enable multi-vector interrupts
    INTConfigureSystem(INT_SYSTEM_CONFIG_MULT_VECTOR);
    INTEnableInterrupts();

    attachCoreTimerService(bamCallback);
    //delay(1);
    attachCoreTimerService(layerCallback);
    //delay(1);
    
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
  
    char fromclient[1024];
    
    // if there's data available, read a packet
    Client client = server.available();

    if(client == true) {

        bytes_read = client.read((uint8_t*)fromclient,1024);
        currentDataPossition = 0; 

        fromclient[bytes_read] = '\0';

        Serial.println(bytes_read);
        Serial.println(fromclient);

        while(currentDataPossition < (bytes_read-2)) {
            ProcessString(fromclient);
        }
    }
}

void ProcessString(char* data) {
    // define the packet [] is 1 byte 0 -> 256
    // [Layer][Pixel][Red][Green][Blue]#

    // read the data from the ethernet stream
    uint8_t readLayer = data[currentDataPossition];
    currentDataPossition++;
    uint8_t readPixel = data[currentDataPossition];
    currentDataPossition++;
    uint8_t readRed = data[currentDataPossition];
    currentDataPossition++;
    uint8_t readGreen = data[currentDataPossition];
    currentDataPossition++;
    uint8_t readBlue = data[currentDataPossition];
    currentDataPossition++;

    // assign the colour read.
    ledArray[readLayer][readPixel][0] = readRed;
    ledArray[readLayer][readPixel][1] = readGreen;
    ledArray[readLayer][readPixel][2] = readBlue;

    // print data
    Serial.print(readLayer);
    Serial.print(" ");
    Serial.print(readPixel);
    Serial.print(" ");
    Serial.print(readRed);
    Serial.print(" ");
    Serial.print(readGreen);
    Serial.print(" ");
    Serial.print(readBlue);
    Serial.print("\n");
}

void SpiSend(uint64_t dataRed, uint64_t dataGreen, uint64_t dataBlue) {

    
    char buf[400];
    sprintf(buf, "SpiSend Red: %016llX Green: %016llX Blue: %016llX", dataRed, dataGreen, dataBlue);
    Serial.println(buf);

    // start communication
    LATECLR = pinSS;

    // for the number of bytes, send through
    for(int i = 0; i < 64; i++) {

        on = 0;

        // clock off
        LATECLR = pinSCK;

        // check the data for Red
        if(dataRed & 1) {
            on = (on | pinMOSIR);
        } 

        //  Green
        if(dataGreen & 1) {
            on = (on | pinMOSIG);
        } 

        // Blue
        if(dataBlue & 1) {
            // on = (on | pinMOSIB);
            Serial.print("b");
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

    // lock the current output
    LATESET = pinSS;

    // reset SPI Communication
    LATECLR = (pinSS|pinMOSIR|pinMOSIG|pinMOSIB|pinSCK);
}

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

        // reset the masks and shifts
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
    
    char buf[400];
    sprintf(buf, "BAM Red: %016llX Green: %016llX Blue: %016llX", dataRed, dataGreen, dataBlue);
    Serial.println(buf);

    // send the colours
    SpiSend(spiRed, spiGreen, spiBlue);
    //SpiSend(0xFFFFFFFFFFFFFFFF,0xFFFFFFFFFFFFFFFF,0xFFFFFFFFFFFFFFFF);
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
    // SpiSend(0xFFFFFFFFFFFFFFFF,0xFFFFFFFFFFFFFFFF,0xFFFFFFFFFFFFFFFF);

    // TODO: There is something weird going on here, changing one pixels
    // colours changes a whole rows, i dont know why this is... but i think
    // its to do with the way i am either accepting data or switching through
    // the layers, may need to use a osciliscope for this.

    // turn off the last layer
    if(layerPossitionCounter == 0) {
        digitalWrite(layerArray[7], 0);
    } else {
        digitalWrite(layerArray[(layerPossitionCounter - 1)], 0);
    }

    // eneable the next layer
    digitalWrite(layerArray[layerPossitionCounter], 1);
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
        // Clear the interrupt flag
        // Red
    
        for (int i = 0; i < 8; ++i)
        {
            for(int j = 0; j < 64; j++) {
                
                if(redchange) {
                    if(ledArray[i][j][0] >= 9) {
                        ledArray[i][j][0] = 0;
                    } else {
                        ledArray[i][j][0] += direction;
                    }
                }

                if(greenchange) {
                    if(ledArray[i][j][1] >= 9) {
                        ledArray[i][j][1] = 0;
                    } else {
                        ledArray[i][j][1] += direction;
                    }
                }
                
                if(bluechange) {
                    if(ledArray[i][j][2] >= 9) {
                        ledArray[i][j][2] = 0;
                    } else {
                        ledArray[i][j][2] += direction;
                    }
                }
            }
        }  
        INTClearFlag(INT_T3);
    }
} 

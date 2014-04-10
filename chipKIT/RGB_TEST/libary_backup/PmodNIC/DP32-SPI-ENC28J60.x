/************************************************************************/
/*																		*/
/*	DP32-SPI-ENC28J60.x                                                */
/*																		*/
/*	Configure the MX3cK for the PmodNIC                     			*/
/*																		*/
/************************************************************************/
/*	Author: 	Keith Vogel 											*/
/*	Copyright 2011, Digilent Inc.										*/
/************************************************************************/
/*
  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/
/************************************************************************/
/*  Revision History:													*/
/*																		*/
/*	5/1/2012(KeithV): Created											*/
/*																		*/
/************************************************************************/
#ifndef DP32_SPI_ENC28J60_X    
#define DP32_SPI_ENC28J60_X    

// Digilent defined values for the MLA build
#define __Digilent_Build__
#define __PIC32MX1XX__ 

// Use PmodNIC, SPI1

// ENC28J60 I/O pins
#define ENC_CS_TRIS			(TRISAbits.TRISA0)          // RA0      ~CS
#define ENC_CS_IO			(LATAbits.LATA0)            // RA0      ~CS
#define ENC_SPI_IF			(IFS0bits.SPI1RXIF)         // RA1      SDI1    SDI1R = 0 
#define ENC_SSPBUF			(SPI1BUF)                   // RB14     SCK1
#define ENC_SPISTATbits		(SPI1STATbits)              // RA4      SDO1    RPA4R = 3  
#define ENC_SPICON1			(SPI1CON)                   
#define ENC_SPICON1bits		(SPI1CONbits)               
#define ENC_SPIBRG			(SPI1BRG)                   
#define ENC_RST_TRIS        (TRISBbits.TRISB5)          // RB5      ~RST  
#define ENC_RST_IO          (LATBbits.LATB5)            // RB5      ~RST
                                                        
static inline void __attribute__((always_inline)) DNETcKInitNetworkHardware(void)
{
    // clear my WiFi bits to make them digital
    ANSELACLR   = 0b0000000000000011;
    ANSELBCLR   = 0b0100000000000000;

    // set up the PPS
    RPA4R = 3;      // SDO1
    SDI1R = 0;      // SDI1          

    ENC_RST_IO          = 1;		
    ENC_RST_TRIS        = 0;

    // Enable the ENC
    ENC_CS_IO           = 1;
    ENC_CS_TRIS         = 0;
}


#endif // DP32_SPI_ENC28J60_X

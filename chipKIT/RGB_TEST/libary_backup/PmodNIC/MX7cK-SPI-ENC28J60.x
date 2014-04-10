/************************************************************************/
/*																		*/
/*	MX7cK-SPI-ENC28J60.x                                                */
/*																		*/
/*	Configure the MX3cK for the PmodNIC			                        */
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
#ifndef MX7cK_SPI_ENC28J60_X
#define MX7cK_SPI_ENC28J60_X

//  JF, SPI4 or SPI3A

// ENC28J60 I/O pins
#define ENC_CS_TRIS			(TRISFbits.TRISF12)	
#define ENC_CS_IO			(LATFbits.LATF12)
#define ENC_SPI_IF			(IFS0bits.SPI4RXIF)
#define ENC_SSPBUF			(SPI4BUF)
#define ENC_SPISTATbits		(SPI4STATbits)
#define ENC_SPICON1			(SPI4CON)
#define ENC_SPICON1bits		(SPI4CONbits)
#define ENC_SPIBRG			(SPI4BRG)

#define ENC_RST_TRIS        (TRISAbits.TRISA4)      // pin 9
#define ENC_RST_IO          (LATAbits.LATA4)

// no analog pins to worry about
#define DNETcKInitNetworkHardware() {ENC_CS_IO = 1;ENC_CS_TRIS = 0;}

#endif // MX7cK_SPI_ENC28J60_X

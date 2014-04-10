/************************************************************************/
/*																		*/
/*	MX4cK-SPI-ENC424J600.x                                              */
/*																		*/
/*	ENC424J600	configuration for the MX4cK 			                */
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
/*	5/2/2012(KeithV): Created											*/
/*																		*/
/************************************************************************/
#ifndef MX4cK_SPI_ENC424J600_X
#define MX4cK_SPI_ENC424J600_X


// ENC624J600 Interface Configuration
// Comment out ENC100_INTERFACE_MODE if you don't have an ENC624J600 or 
// ENC424J600.  Otherwise, choose the correct setting for the interface you 
// are using.  Legal values are:
//  - Commented out: No ENC424J600/624J600 present or used.  All other 
//                   ENC100_* macros are ignored.
//	- 0: SPI mode using CS, SCK, SI, and SO pins
//  - 1: 8-bit demultiplexed PSP Mode 1 with RD and WR pins
//  - 2: *8-bit demultiplexed PSP Mode 2 with R/Wbar and EN pins
//  - 3: *16-bit demultiplexed PSP Mode 3 with RD, WRL, and WRH pins
//  - 4: *16-bit demultiplexed PSP Mode 4 with R/Wbar, B0SEL, and B1SEL pins
//  - 5: 8-bit multiplexed PSP Mode 5 with RD and WR pins
//  - 6: *8-bit multiplexed PSP Mode 6 with R/Wbar and EN pins
//  - 9: 16-bit multiplexed PSP Mode 9 with AL, RD, WRL, and WRH pins
//  - 10: *16-bit multiplexed PSP Mode 10 with AL, R/Wbar, B0SEL, and B1SEL 
//        pins
// *IMPORTANT NOTE: DO NOT USE PSP MODE 2, 4, 6, OR 10 ON EXPLORER 16! 
// Attempting to do so will cause bus contention with the LCD module which 
// shares the PMP.  Also, PSP Mode 3 is risky on the Explorer 16 since it 
// can randomly cause bus contention with the 25LC256 EEPROM.
#define ENC100_INTERFACE_MODE			0

// JB, SPI2, INT3

#define ENC100_CS_TRIS			(TRISGbits.TRISG9)	
#define ENC100_CS_IO			(LATGbits.LATG9)
#define ENC100_ISR_ENABLE		(IEC0bits.INT3IE)
#define ENC100_ISR_FLAG			(IFS0bits.INT3IF)
#define ENC100_ISR_POLARITY		(INTCONbits.INT3EP)
#define ENC100_ISR_PRIORITY		(IPC2bits.INT3IP)
#define ENC100_SPI_ENABLE		(ENC100_SPICON1bits.ON)
#define ENC100_SPI_IF			(IFS0bits.SPI2RXIF)
#define ENC100_SSPBUF			(SPI2BUF)
#define ENC100_SPICON1			(SPI2CON)
#define ENC100_SPISTATbits		(SPI2STATbits)
#define ENC100_SPICON1bits		(SPI2CONbits)
#define ENC100_SPIBRG			(SPI2BRG)

#define DNETcKInitNetworkHardware() {ENC100_CS_IO = 1;ENC100_CS_TRIS = 0;}

#endif // MX4cK_SPI_ENC424J600_X

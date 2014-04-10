/************************************************************************/
/*																		*/
/*	NetworkProfile.x                                                    */
/*																		*/
/*	Network Hardware vector file for the PmodNIC                    	*/
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

#ifndef PMODNIC_NETWORK_PROFILE_X
#define PMODNIC_NETWORK_PROFILE_X

#define DNETcK_LAN_Hardware
#define _DNETcK_ENC28J60

// board specific stuff
#if defined(_BOARD_UNO_)

    #include <Uno32-SPI-ENC28J60.x>

#elif defined(_BOARD_UC32_) || defined(_BOARD_CEREBOT_MX3CK_512_)

    #include <uC32-SPI-ENC28J60.x>

#elif defined (_BOARD_MEGA_)

    #include <Max32-SPI-ENC28J60.x>

#elif defined  (_BOARD_CEREBOT_MX3CK_)

    #include <MX3cK-SPI-ENC28J60.x>

#elif defined  (_BOARD_CEREBOT_MX4CK_) || defined (_BOARD_CEREBOT_32MX4_)

    #include <MX4cK-SPI-ENC28J60.x>

#elif defined  (_BOARD_CEREBOT_MX7CK_) || defined (_BOARD_CEREBOT_32MX7_)

    #include <MX7cK-SPI-ENC28J60.x>

#elif defined (_BOARD_CMOD_)

    #include <Cmod-SPI-ENC28J60.x>

#elif defined (_BOARD_DP32_)

    #include <DP32-SPI-ENC28J60.x>

#else

    #error PmodNIC is not supported by this board.

#endif

#endif // PMODNIC_NETWORK_PROFILE_X

/************************************************************************/
/*																		*/
/*	TCPIPConfig.x                                                       */
/*																		*/
/*	TCPIP Config vector file for the Network Shield						*/
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
/*	3/22/2012(KeithV): Created											*/
/*																		*/
/************************************************************************/

#ifndef NetworkShield_TCPIPConfig_X
#define NetworkShield_TCPIPConfig_X

// board specific stuff
#if defined (_BOARD_MEGA_)

    #include <Max32-SMSC-8720-TCPIPConfig.x>

//For convenience the MX7cK as it is the same hardware.
#elif defined (_BOARD_CEREBOT_MX7CK_)

    #include <MX7cK-SMSC-8720-TCPIPConfig.x>

#elif defined (_BOARD_CEREBOT_32MX7_)

    #include <32MX7-SMSC-8720-TCPIPConfig.x>

#else

    #error NetworkShield is not supported by this board.

#endif

#endif // NetworkShield_TCPIPConfig_X

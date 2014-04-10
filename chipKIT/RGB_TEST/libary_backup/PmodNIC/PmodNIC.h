/************************************************************************/
/*                                                                      */
/*    PmodNIC100.h                                                      */
/*                                                                      */
/*    Include this file in a sketch to cause MPIDE to put this library  */
/*    first in the -I include list so NetworkProfile.x and TCPConfig.x  */
/*    will be found her before any other directory after in the list.   */
/*                                                                      */
/*    Supports:                                                         */
/* Cmod with pmodNIC on connector J1                                    */
/* DP32 with pmodNIC   CS-RA0, MISO-RA1, MOSI-RA4, SCK-RB14, RST-RB5    */
/* Uno32 JP5&7 on Master with PmodShield and PmodNIC on connector JC    */
/* uC32 JP5&7 on Master with PmodShield and PmodNIC on connector JC     */
/* Max32 JP3&4 on Master with PmodShield and PmodNIC on connector JC    */
/* MX3cK JP6&8 on Master with PmodNIC on connector JE                   */
/* MX3cK-512 JP6&8 on Master with PmodNIC on connector JE               */
/* MX4ck JP3 on INT3 with PmodNIC on connector JB                       */
/* MX7ck with PmodNIC on connector JF                                   */
/* 32MX4 with PmodNIC with X-over cable on connector JB                 */
/* 32MX7 with PmodNIC on connector JF                                   */
/*                                                                      */
/************************************************************************/
/*    Author:     Keith Vogel                                           */
/*    Copyright 2011, Digilent Inc.                                     */
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
/*  Revision History:                                                   */
/*                                                                      */
/*    5/2/2012(KeithV): Created                                         */
/*                                                                      */
/************************************************************************/
#ifndef PMODNIC_H
#define PMODNIC_H

#if defined(DNETcK_Network_Hardware)
    #error Multiple network hardwares are included, select only one.
#elif defined(_DNETCK_H)
    #error DNETcK.h must be included after PmodNIC.h.
#elif defined( _DWIFICK_H)
    #error WiFi is incompatible with a PmodNIC.
#endif

#define DNETcK_Network_Hardware
#define DNETcK_PmodNIC

#endif // PMODNIC_H
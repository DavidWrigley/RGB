/************************************************************************/
/*                                                                      */
/*    NetworkShield.h                                                   */
/*                                                                      */
/*    NetworkShield library include file to be used with DNETck         */
/*                                                                      */
/*    Supports:                                                         */
/*        Max32 with Network Shield                                     */
/*        MX7ck and the on board NIC                                    */
/*        32MX7 and the on board NIC                                    */
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
/*    4/26/2012(KeithV): Created                                        */
/*                                                                      */
/************************************************************************/
#ifndef NetworkShield_H
#define NetworkShield_H

#if defined(DNETcK_Network_Hardware)
    #error Multiple network hardwares are included, select only one.
#elif defined(_DNETCK_H)
    #error DNETcK.h must be included after NetworkShield.h.
#elif defined( _DWIFICK_H)
    #error WiFi is incompatible with a NetworkShield.
#endif

#define DNETcK_Network_Hardware
#define DNETcK_NetworkShield

#endif // NetworkShield_H
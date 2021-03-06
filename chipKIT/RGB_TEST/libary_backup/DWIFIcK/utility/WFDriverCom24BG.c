/************************************************************************/
/*																		*/
/*	WFDriverCom24BG.c                                                   */
/*																		*/
/*	Vector file for either B or G MRF24W   	                            */
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
/*	10/16/2012(KeithV): Created											*/
/*																		*/
/************************************************************************/
#include "HardwareProfile.h"

#if defined(MRF24WG)
	#include "MRF24WG/WFDriverCom_24G.c"
#else
	#include "MRF24WB/WFDriverCom.c"
#endif
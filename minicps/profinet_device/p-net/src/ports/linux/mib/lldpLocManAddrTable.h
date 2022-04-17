/*********************************************************************
 *        _       _         _
 *  _ __ | |_  _ | |  __ _ | |__   ___
 * | '__|| __|(_)| | / _` || '_ \ / __|
 * | |   | |_  _ | || (_| || |_) |\__ \
 * |_|    \__|(_)|_| \__,_||_.__/ |___/
 *
 * www.rt-labs.com
 * Copyright 2020 rt-labs AB, Sweden.
 *
 * This software is dual-licensed under GPLv3 and a commercial
 * license. See the file LICENSE.md distributed with this software for
 * full license information.
 ********************************************************************/

/*
 * Note: this file originally auto-generated by mib2c
 * using mib2c.iterate.conf
 */
#ifndef LLDPLOCMANADDRTABLE_H
#define LLDPLOCMANADDRTABLE_H

#include "pf_includes.h"

/* function declarations */
void init_lldpLocManAddrTable (pnet_t * pnet);
void initialize_table_lldpLocManAddrTable (pnet_t * pnet);
Netsnmp_Node_Handler lldpLocManAddrTable_handler;
Netsnmp_First_Data_Point lldpLocManAddrTable_get_first_data_point;
Netsnmp_Next_Data_Point lldpLocManAddrTable_get_next_data_point;

/* column number definitions for table lldpLocManAddrTable */
#define COLUMN_LLDPLOCMANADDRSUBTYPE   1
#define COLUMN_LLDPLOCMANADDR          2
#define COLUMN_LLDPLOCMANADDRLEN       3
#define COLUMN_LLDPLOCMANADDRIFSUBTYPE 4
#define COLUMN_LLDPLOCMANADDRIFID      5
#define COLUMN_LLDPLOCMANADDROID       6
#endif /* LLDPLOCMANADDRTABLE_H */

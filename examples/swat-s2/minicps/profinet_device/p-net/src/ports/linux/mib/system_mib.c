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
 * using mib2c.scalar.conf
 */

#include <net-snmp/net-snmp-config.h>
#include <net-snmp/net-snmp-includes.h>
#include <net-snmp/agent/net-snmp-agent-includes.h>

#undef LOG_DEBUG
#undef LOG_WARNING
#undef LOG_INFO
#undef LOG_ERROR
#undef LOG_FATAL

#include "system_mib.h"

#include <sys/sysinfo.h>

/** Initializes the system_mib module */
void init_system_mib (pnet_t * pnet)
{
   const oid sysDescr_oid[] = {1, 3, 6, 1, 2, 1, 1, 1};
   const oid sysObjectID_oid[] = {1, 3, 6, 1, 2, 1, 1, 2};
   const oid sysUpTime_oid[] = {1, 3, 6, 1, 2, 1, 1, 3};
   const oid sysContact_oid[] = {1, 3, 6, 1, 2, 1, 1, 4};
   const oid sysName_oid[] = {1, 3, 6, 1, 2, 1, 1, 5};
   const oid sysLocation_oid[] = {1, 3, 6, 1, 2, 1, 1, 6};
   const oid sysServices_oid[] = {1, 3, 6, 1, 2, 1, 1, 7};
   netsnmp_handler_registration * reg;

   netsnmp_register_scalar (
      reg = netsnmp_create_handler_registration (
         "sysDescr",
         handle_sysDescr,
         sysDescr_oid,
         OID_LENGTH (sysDescr_oid),
         HANDLER_CAN_RONLY));

   reg->my_reg_void = pnet;

   netsnmp_register_scalar (
      reg = netsnmp_create_handler_registration (
         "sysObjectID",
         handle_sysObjectID,
         sysObjectID_oid,
         OID_LENGTH (sysObjectID_oid),
         HANDLER_CAN_RONLY));

   reg->my_reg_void = pnet;

   netsnmp_register_scalar (
      reg = netsnmp_create_handler_registration (
         "sysUpTime",
         handle_sysUpTime,
         sysUpTime_oid,
         OID_LENGTH (sysUpTime_oid),
         HANDLER_CAN_RONLY));

   reg->my_reg_void = pnet;

   netsnmp_register_scalar (
      reg = netsnmp_create_handler_registration (
         "sysContact",
         handle_sysContact,
         sysContact_oid,
         OID_LENGTH (sysContact_oid),
         HANDLER_CAN_RWRITE));

   reg->my_reg_void = pnet;

   netsnmp_register_scalar (
      reg = netsnmp_create_handler_registration (
         "sysName",
         handle_sysName,
         sysName_oid,
         OID_LENGTH (sysName_oid),
         HANDLER_CAN_RWRITE));

   reg->my_reg_void = pnet;

   netsnmp_register_scalar (
      reg = netsnmp_create_handler_registration (
         "sysLocation",
         handle_sysLocation,
         sysLocation_oid,
         OID_LENGTH (sysLocation_oid),
         HANDLER_CAN_RWRITE));

   reg->my_reg_void = pnet;

   netsnmp_register_scalar (
      reg = netsnmp_create_handler_registration (
         "sysServices",
         handle_sysServices,
         sysServices_oid,
         OID_LENGTH (sysServices_oid),
         HANDLER_CAN_RONLY));

   reg->my_reg_void = pnet;
}

int handle_sysDescr (
   netsnmp_mib_handler * handler,
   netsnmp_handler_registration * reginfo,
   netsnmp_agent_request_info * reqinfo,
   netsnmp_request_info * requests)
{
   pnet_t * pnet = reginfo->my_reg_void;
   pf_snmp_system_description_t sysdescription;

   /* We are never called for a GETNEXT if it's registered as a
      "instance", as it's "magically" handled for us.  */

   /* a instance handler also only hands us one request at a time, so
      we don't need to loop over a list of requests; we'll only get one. */

   pf_snmp_get_system_description (pnet, &sysdescription);

   switch (reqinfo->mode)
   {

   case MODE_GET:
      LOG_DEBUG (PF_SNMP_LOG, "system_mib(%d): GET sysDescr.\n", __LINE__);
      snmp_set_var_typed_value (
         requests->requestvb,
         ASN_OCTET_STR,
         sysdescription.string,
         strlen (sysdescription.string));
      break;

   default:
      /* we should never get here, so this is a really bad error */
      LOG_ERROR (
         PF_SNMP_LOG,
         "system_mib(%d): unknown mode (%d)\n",
         __LINE__,
         reqinfo->mode);
      return SNMP_ERR_GENERR;
   }

   return SNMP_ERR_NOERROR;
}
int handle_sysObjectID (
   netsnmp_mib_handler * handler,
   netsnmp_handler_registration * reginfo,
   netsnmp_agent_request_info * reqinfo,
   netsnmp_request_info * requests)
{
   const oid sysoid[] = {1, 3, 6, 1, 4, 1, 24686};

   /* We are never called for a GETNEXT if it's registered as a
      "instance", as it's "magically" handled for us.  */

   /* a instance handler also only hands us one request at a time, so
      we don't need to loop over a list of requests; we'll only get one. */

   switch (reqinfo->mode)
   {

   case MODE_GET:
      LOG_DEBUG (PF_SNMP_LOG, "system_mib(%d): GET sysObjectID.\n", __LINE__);
      snmp_set_var_typed_value (
         requests->requestvb,
         ASN_OBJECT_ID,
         sysoid,
         OID_LENGTH (sysoid) * sizeof (oid));
      break;

   default:
      /* we should never get here, so this is a really bad error */
      LOG_ERROR (
         PF_SNMP_LOG,
         "system_mib(%d): unknown mode (%d)\n",
         __LINE__,
         reqinfo->mode);
      return SNMP_ERR_GENERR;
   }

   return SNMP_ERR_NOERROR;
}

int handle_sysUpTime (
   netsnmp_mib_handler * handler,
   netsnmp_handler_registration * reginfo,
   netsnmp_agent_request_info * reqinfo,
   netsnmp_request_info * requests)
{
   struct sysinfo systeminfo; /* Field .uptime contains uptime in seconds */
   uint32_t uptime_10ms;

   /* We are never called for a GETNEXT if it's registered as a
      "instance", as it's "magically" handled for us.  */

   /* a instance handler also only hands us one request at a time, so
      we don't need to loop over a list of requests; we'll only get one. */

   switch (reqinfo->mode)
   {
   case MODE_GET:
      LOG_DEBUG (PF_SNMP_LOG, "system_mib(%d): GET sysUpTime.\n", __LINE__);
      if (sysinfo (&systeminfo) == 0)
      {
         uptime_10ms = systeminfo.uptime * 100;
      }
      else
      {
         uptime_10ms = 0;
      }

      snmp_set_var_typed_integer (
         requests->requestvb,
         ASN_TIMETICKS,
         uptime_10ms);
      break;

   default:
      /* we should never get here, so this is a really bad error */
      LOG_ERROR (
         PF_SNMP_LOG,
         "system_mib(%d): unknown mode (%d)\n",
         __LINE__,
         reqinfo->mode);
      return SNMP_ERR_GENERR;
   }

   return SNMP_ERR_NOERROR;
}

int handle_sysContact (
   netsnmp_mib_handler * handler,
   netsnmp_handler_registration * reginfo,
   netsnmp_agent_request_info * reqinfo,
   netsnmp_request_info * requests)
{
   int ret;
   pnet_t * pnet = reginfo->my_reg_void;
   pf_snmp_system_contact_t syscontact;
   static pf_snmp_system_contact_t * old_syscontact;

   /* We are never called for a GETNEXT if it's registered as a
      "instance", as it's "magically" handled for us.  */

   /* a instance handler also only hands us one request at a time, so
      we don't need to loop over a list of requests; we'll only get one. */

   LOG_DEBUG (
      PF_SNMP_LOG,
      "system_mib(%d): Handle sysContact. Mode: %d\n",
      __LINE__,
      reqinfo->mode);

   switch (reqinfo->mode)
   {

   case MODE_GET:
      pf_snmp_get_system_contact (pnet, &syscontact);
      snmp_set_var_typed_value (
         requests->requestvb,
         ASN_OCTET_STR,
         syscontact.string,
         strlen (syscontact.string));
      break;

   /*
    * SET REQUEST
    *
    * multiple states in the transaction.  See:
    * http://www.net-snmp.org/tutorial/tutorial-5/toolkit/mib_module/set-actions.jpg
    */
   case MODE_SET_RESERVE1:
      old_syscontact = NULL;
      ret = netsnmp_check_vb_type_and_max_size (
         requests->requestvb,
         ASN_OCTET_STR,
         sizeof (syscontact.string) - 1);
      if (ret != SNMP_ERR_NOERROR)
      {
         netsnmp_set_request_error (reqinfo, requests, ret);
      }
      break;

   case MODE_SET_RESERVE2:
      old_syscontact = SNMP_MALLOC_TYPEDEF (pf_snmp_system_contact_t);
      if (old_syscontact == NULL)
      {
         netsnmp_set_request_error (
            reqinfo,
            requests,
            SNMP_ERR_RESOURCEUNAVAILABLE);
      }
      else
      {
         pf_snmp_get_system_contact (pnet, old_syscontact);
      }
      break;

   case MODE_SET_FREE:
      if (old_syscontact != NULL)
      {
         SNMP_FREE (old_syscontact);
      }
      break;

   case MODE_SET_ACTION:
      memcpy (
         syscontact.string,
         requests->requestvb->val.string,
         requests->requestvb->val_len);
      syscontact.string[requests->requestvb->val_len] = '\0';
      ret = pf_snmp_set_system_contact (pnet, &syscontact);
      if (ret)
      {
         netsnmp_set_request_error (reqinfo, requests, SNMP_ERR_GENERR);
      }
      break;

   case MODE_SET_COMMIT:
      SNMP_FREE (old_syscontact);
      break;

   case MODE_SET_UNDO:
      ret = pf_snmp_set_system_contact (pnet, old_syscontact);
      if (ret)
      {
         netsnmp_set_request_error (reqinfo, requests, SNMP_ERR_UNDOFAILED);
      }
      SNMP_FREE (old_syscontact);
      break;

   default:
      /* we should never get here, so this is a really bad error */
      LOG_ERROR (
         PF_SNMP_LOG,
         "system_mib(%d): unknown mode (%d)\n",
         __LINE__,
         reqinfo->mode);
      return SNMP_ERR_GENERR;
   }

   return SNMP_ERR_NOERROR;
}

int handle_sysName (
   netsnmp_mib_handler * handler,
   netsnmp_handler_registration * reginfo,
   netsnmp_agent_request_info * reqinfo,
   netsnmp_request_info * requests)
{
   int ret;
   pnet_t * pnet = reginfo->my_reg_void;
   pf_snmp_system_name_t sysname;
   static pf_snmp_system_name_t * old_sysname;

   /* We are never called for a GETNEXT if it's registered as a
      "instance", as it's "magically" handled for us.  */

   /* a instance handler also only hands us one request at a time, so
      we don't need to loop over a list of requests; we'll only get one. */

   LOG_DEBUG (
      PF_SNMP_LOG,
      "system_mib(%d): Handle sysName. Mode: %d\n",
      __LINE__,
      reqinfo->mode);

   switch (reqinfo->mode)
   {

   case MODE_GET:
      pf_snmp_get_system_name (pnet, &sysname);
      snmp_set_var_typed_value (
         requests->requestvb,
         ASN_OCTET_STR,
         sysname.string,
         strlen (sysname.string));
      break;

   /*
    * SET REQUEST
    *
    * multiple states in the transaction.  See:
    * http://www.net-snmp.org/tutorial/tutorial-5/toolkit/mib_module/set-actions.jpg
    */
   case MODE_SET_RESERVE1:
      old_sysname = NULL;
      ret = netsnmp_check_vb_type_and_max_size (
         requests->requestvb,
         ASN_OCTET_STR,
         sizeof (sysname.string) - 1);
      if (ret != SNMP_ERR_NOERROR)
      {
         netsnmp_set_request_error (reqinfo, requests, ret);
      }
      break;

   case MODE_SET_RESERVE2:
      old_sysname = SNMP_MALLOC_TYPEDEF (pf_snmp_system_name_t);
      if (old_sysname == NULL)
      {
         netsnmp_set_request_error (
            reqinfo,
            requests,
            SNMP_ERR_RESOURCEUNAVAILABLE);
      }
      else
      {
         pf_snmp_get_system_name (pnet, old_sysname);
      }
      break;

   case MODE_SET_FREE:
      if (old_sysname != NULL)
      {
         SNMP_FREE (old_sysname);
      }
      break;

   case MODE_SET_ACTION:
      memcpy (
         sysname.string,
         requests->requestvb->val.string,
         requests->requestvb->val_len);
      sysname.string[requests->requestvb->val_len] = '\0';
      ret = pf_snmp_set_system_name (pnet, &sysname);
      if (ret)
      {
         netsnmp_set_request_error (reqinfo, requests, SNMP_ERR_GENERR);
      }
      break;

   case MODE_SET_COMMIT:
      SNMP_FREE (old_sysname);
      break;

   case MODE_SET_UNDO:
      ret = pf_snmp_set_system_name (pnet, old_sysname);
      if (ret)
      {
         netsnmp_set_request_error (reqinfo, requests, SNMP_ERR_UNDOFAILED);
      }
      SNMP_FREE (old_sysname);
      break;

   default:
      /* we should never get here, so this is a really bad error */
      LOG_ERROR (
         PF_SNMP_LOG,
         "system_mib(%d): unknown mode (%d)\n",
         __LINE__,
         reqinfo->mode);
      return SNMP_ERR_GENERR;
   }

   return SNMP_ERR_NOERROR;
}

int handle_sysLocation (
   netsnmp_mib_handler * handler,
   netsnmp_handler_registration * reginfo,
   netsnmp_agent_request_info * reqinfo,
   netsnmp_request_info * requests)
{
   int ret;
   pnet_t * pnet = reginfo->my_reg_void;
   pf_snmp_system_location_t syslocation;
   static pf_snmp_system_location_t * old_syslocation;

   /* We are never called for a GETNEXT if it's registered as a
      "instance", as it's "magically" handled for us.  */

   /* a instance handler also only hands us one request at a time, so
      we don't need to loop over a list of requests; we'll only get one. */

   LOG_DEBUG (
      PF_SNMP_LOG,
      "system_mib(%d): Handle sysLocation. Mode: %d\n",
      __LINE__,
      reqinfo->mode);

   switch (reqinfo->mode)
   {

   case MODE_GET:
      pf_snmp_get_system_location (pnet, &syslocation);
      snmp_set_var_typed_value (
         requests->requestvb,
         ASN_OCTET_STR,
         syslocation.string,
         strlen (syslocation.string));
      break;

   /*
    * SET REQUEST
    *
    * multiple states in the transaction.  See:
    * http://www.net-snmp.org/tutorial/tutorial-5/toolkit/mib_module/set-actions.jpg
    */
   case MODE_SET_RESERVE1:
      old_syslocation = NULL;
      ret = netsnmp_check_vb_type_and_max_size (
         requests->requestvb,
         ASN_OCTET_STR,
         sizeof (syslocation.string) - 1);
      if (ret != SNMP_ERR_NOERROR)
      {
         netsnmp_set_request_error (reqinfo, requests, ret);
      }
      break;

   case MODE_SET_RESERVE2:
      old_syslocation = SNMP_MALLOC_TYPEDEF (pf_snmp_system_location_t);
      if (old_syslocation == NULL)
      {
         netsnmp_set_request_error (
            reqinfo,
            requests,
            SNMP_ERR_RESOURCEUNAVAILABLE);
      }
      else
      {
         pf_snmp_get_system_location (pnet, old_syslocation);
      }
      break;

   case MODE_SET_FREE:
      if (old_syslocation != NULL)
      {
         SNMP_FREE (old_syslocation);
      }
      break;

   case MODE_SET_ACTION:
      memcpy (
         syslocation.string,
         requests->requestvb->val.string,
         requests->requestvb->val_len);
      syslocation.string[requests->requestvb->val_len] = '\0';
      ret = pf_snmp_set_system_location (pnet, &syslocation);
      if (ret)
      {
         netsnmp_set_request_error (reqinfo, requests, SNMP_ERR_GENERR);
      }
      break;

   case MODE_SET_COMMIT:
      SNMP_FREE (old_syslocation);
      break;

   case MODE_SET_UNDO:
      ret = pf_snmp_set_system_location (pnet, old_syslocation);
      if (ret)
      {
         netsnmp_set_request_error (reqinfo, requests, SNMP_ERR_UNDOFAILED);
      }
      SNMP_FREE (old_syslocation);
      break;

   default:
      /* we should never get here, so this is a really bad error */
      LOG_ERROR (
         PF_SNMP_LOG,
         "system_mib(%d): unknown mode (%d)\n",
         __LINE__,
         reqinfo->mode);
      return SNMP_ERR_GENERR;
   }

   return SNMP_ERR_NOERROR;
}

int handle_sysServices (
   netsnmp_mib_handler * handler,
   netsnmp_handler_registration * reginfo,
   netsnmp_agent_request_info * reqinfo,
   netsnmp_request_info * requests)
{
   /* We are never called for a GETNEXT if it's registered as a
      "instance", as it's "magically" handled for us.  */

   /* a instance handler also only hands us one request at a time, so
      we don't need to loop over a list of requests; we'll only get one. */

   switch (reqinfo->mode)
   {

   case MODE_GET:
      LOG_DEBUG (PF_SNMP_LOG, "system_mib(%d): GET sysServices\n", __LINE__);
      /* Supported services. Should be 78 for Profinet. See IETF RFC 3418. */
      snmp_set_var_typed_integer (requests->requestvb, ASN_INTEGER, 78);
      break;

   default:
      /* we should never get here, so this is a really bad error */
      LOG_ERROR (
         PF_SNMP_LOG,
         "system_mib(%d): unknown mode (%d)\n",
         __LINE__,
         reqinfo->mode);
      return SNMP_ERR_GENERR;
   }

   return SNMP_ERR_NOERROR;
}

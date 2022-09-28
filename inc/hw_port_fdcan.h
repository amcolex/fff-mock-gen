/**======================================= (c) Flyability ==========================================
 **-------------------------------------------------------------------------------------------------
 **  File Description: Management of FDCAN peripherals.
 **===============================================================================================*/
#pragma once
/**=================================================================================================
 **                                 Includes / Defines / Macros
 **===============================================================================================*/
#include <stdint.h>
#include <hal_drivers.h>
/**=================================================================================================
 **                             Public Typedefs / Constants / Macros
 **===============================================================================================*/
typedef void (*hw_can_data_frame_callback_t)(uint32_t extended_id, const uint8_t* payload,
                                             uint8_t payload_length);
/**=================================================================================================
 **                                       Public Functions
 **===============================================================================================*/
void hw_fdcan_bat_init(void);
hal_flag_t hw_bat_send(uint32_t extended_id, const uint8_t* payload, uint16_t payload_length);
void hw_can_register_receive_callback(hw_can_data_frame_callback_t function);
uint8_t hw_can_send_data_frame(uint32_t extended_id, const uint8_t* payload,
                               uint16_t payload_length, uint32_t timeout);
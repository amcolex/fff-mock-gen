/**======================================= (c) Flyability ==========================================
 **-------------------------------------------------------------------------------------------------
 **  File Description: Management of general peripherals. Dedicated files for several types of
 **                     peripherals exist as hw_port_*.
 **===============================================================================================*/

/**=================================================================================================
 **                                 Includes / Defines / Macros
 **===============================================================================================*/
#include <stdbool.h>
#include <stdint.h>
/**=================================================================================================
 **                                       Public Functions
 **===============================================================================================*/

_Noreturn void hw_send_drone_to_standby_mode(void);
bool hw_is_waking_up_from_standby(void);
void hw_init(void);

// Status leds and user button
void hw_set_status_leds(uint8_t led_red, uint8_t led_green, uint8_t led_blue);

// Watchdog Reset
void hw_start_watchdog_reset(void);
void hw_refresh_watchdog_reset(void);
void mcu_sw_reset(void);
bool hw_watchdog_was_triggered(void);
void hw_reset_watchdog_triggered_flag(void);
void hw_set_backup_register0(uint32_t value);
uint32_t hw_get_backup_register0(void);
void hw_set_backup_register1(uint32_t value);
uint32_t hw_get_backup_register1(void);
void mcu_sw_reset(void);
uint32_t hw_get_uid_1(void);

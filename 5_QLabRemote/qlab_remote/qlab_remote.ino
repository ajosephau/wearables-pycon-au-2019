/*********************************************************************
  This is an example for our nRF51822 based Bluefruit LE modules

  Pick one up today in the adafruit shop!

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  MIT license, check LICENSE for more information
  All text above, and the splash screen below must be included in
  any redistribution
*********************************************************************/

#include <Arduino.h>
#include <SPI.h>
#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_SPI.h"
#include "Adafruit_BluefruitLE_UART.h"
#include <Adafruit_NeoPixel.h>

#include "BluefruitConfig.h"

#if SOFTWARE_SERIAL_AVAILABLE
#include <SoftwareSerial.h>
#endif

#define NEOPIXEL_PIN 8

#define D10_BUTTON_PIN 10
#define D12_BUTTON_PIN 12

/*=========================================================================
    APPLICATION SETTINGS

      FACTORYRESET_ENABLE       Perform a factory reset when running this sketch
     
                                Enabling this will put your Bluefruit LE module
                              in a 'known good' state and clear any config
                              data set in previous sketches or projects, so
                                running this at least once is a good idea.
     
                                When deploying your project, however, you will
                              want to disable factory reset by setting this
                              value to 0.  If you are making changes to your
                                Bluefruit LE device via AT commands, and those
                              changes aren't persisting across resets, this
                              is the reason why.  Factory reset will erase
                              the non-volatile memory where config data is
                              stored, setting it back to factory default
                              values.
         
                                Some sketches that require you to bond to a
                              central device (HID mouse, keyboard, etc.)
                              won't work at all with this feature enabled
                              since the factory reset will clear all of the
                              bonding data stored on the chip, meaning the
                              central device won't be able to reconnect.
    MINIMUM_FIRMWARE_VERSION  Minimum firmware version to have some new features
    -----------------------------------------------------------------------*/
#define FACTORYRESET_ENABLE         0
#define MINIMUM_FIRMWARE_VERSION    "0.6.6"
/*=========================================================================*/


// Create the bluefruit object, either software serial...uncomment these lines

/* ...or hardware serial, which does not need the RTS/CTS pins. Uncomment this line */
Adafruit_BluefruitLE_UART ble(BLUEFRUIT_HWSERIAL_NAME, BLUEFRUIT_UART_MODE_PIN);

Adafruit_NeoPixel strip = Adafruit_NeoPixel(1, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

int neopixel_mode = 0;


/**************************************************************************/
/*!
    @brief  Sets up the HW an the BLE module (this function is called
            automatically on startup)
*/
/**************************************************************************/
void setup(void)
{
  ble.begin(VERBOSE_MODE);

  if ( FACTORYRESET_ENABLE )
  {
    /* Perform a factory reset to make sure everything is in a known state */
    ble.factoryReset();
  }

  /* Disable command echo from Bluefruit */
  ble.echo(false);

  ble.info();

  /* Change the device name to make it easier to find */
  ble.sendCommandCheckOK(F( "AT+GAPDEVNAME=QLab Remote" ));

  /* Enable HID Service */
  if ( ble.isVersionAtLeast(MINIMUM_FIRMWARE_VERSION) )
  {
    ble.sendCommandCheckOK(F( "AT+BleHIDEn=On" ));
  } else
  {
    ble.sendCommandCheckOK(F( "AT+BleKeyboardEn=On"  ));
  }

  /* Add or remove service requires a reset */
  ble.reset();

  /* setup input pins */
  pinMode(D10_BUTTON_PIN, INPUT);
  pinMode(D12_BUTTON_PIN, INPUT);
  digitalWrite(D10_BUTTON_PIN, HIGH);
  digitalWrite(D12_BUTTON_PIN, HIGH);

  /* setup LED */
  strip.begin();
  strip.setBrightness(50);
  strip.show(); // Initialize all pixels to 'off'
}

/**************************************************************************/
/*!
    @brief  Constantly poll for new command or response data
*/
/**************************************************************************/
void loop(void)
{
  if (digitalRead(D12_BUTTON_PIN) == LOW) {
    ble.println("AT+BLEKEYBOARDCODE=00-00-05-00-00");
    ble.println("AT+BLEKEYBOARDCODE=00-00");
    neopixel_mode = 1;
    ble.waitForOK();
  }
  else if (digitalRead(D10_BUTTON_PIN) == LOW) {
    ble.println("AT+BLEKEYBOARDCODE=00-00-0A-00-00");
    ble.println("AT+BLEKEYBOARDCODE=00-00");
    neopixel_mode = 2;
    ble.waitForOK();
  }
  else {
    neopixel_mode = 0;
  }

  if (neopixel_mode == 1) {
    colorWipe(strip.Color(255, 0, 0)); // Red
  }
  else if (neopixel_mode == 2) {
    colorWipe(strip.Color(0, 255, 0)); // Green
  }
  else {
    colorWipe(strip.Color(0, 0, 255)); // Blue
  }
  delay(500);
}


/**************************************************************************/
/*!
    @brief  sets colour of neopixel
*/
/**************************************************************************/
void colorWipe(uint32_t c) {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
  }
}

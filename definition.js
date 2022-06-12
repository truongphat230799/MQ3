Blockly.Blocks['mq3_get_ppm'] = {
    init: function() {
      this.jsonInit(
        {
          "message0": "đọc giá trị nồng độ ppm chân %1",
          "args0": [
            {
              "type": "field_dropdown",
              "name": "NAME",
              "options": [
                [
                  "P0",
                  "pin0"
                ],
                [
                  "P1",
                  "pin1"
                ],
                [
                  "P2",
                  "pin2"
                ]
              ]
            }
          ],
          "output": null,
          "colour": "#6642bf",
          "helpUrl": ""
        }
      );
    },
    getDeveloperVars: function() {
      return ['mq3'];
    }
    
  };
  
  Blockly.Python['mq3_get_ppm'] = function(block) {
    var dropdown_name = block.getFieldValue('NAME');
    Blockly.Python.definitions_['import_yolobit'] = 'from yolobit import *';
    Blockly.Python.definitions_['import_i2c'] = 'from machine import Pin';
    Blockly.Python.definitions_['import_mq3'] = 'from mq3 import MQ3';
    Blockly.Python.definitions_["import_create_mq3"] = 'mq3 = MQ3(Pin(' + dropdown_name + '.adc_pin)) # analog PIN';
    // TODO: Assemble Python into code variable.
    var code = 'mq3.get_ppm()';
    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Blockly.Python.ORDER_NONE];
  };

  Blockly.Blocks['mq3_get_acohol'] = {
    init: function() {
      this.jsonInit(
        {
          "message0": "đọc giá trị nồng độ cồn chân %1",
          "args0": [
            {
              "type": "field_dropdown",
              "name": "NAME",
              "options": [
                [
                  "P0",
                  "pin0"
                ],
                [
                  "P1",
                  "pin1"
                ],
                [
                  "P2",
                  "pin2"
                ]
              ]
            }
          ],
          "output": null,
          "colour": "#6642bf",
          "helpUrl": ""
        }
      );
    },
    getDeveloperVars: function() {
      return ['mq3'];
    }
    
  };
  
  Blockly.Python['mq3_get_acohol'] = function(block) {
    var dropdown_name = block.getFieldValue('NAME');
    Blockly.Python.definitions_['import_yolobit'] = 'from yolobit import *';
    Blockly.Python.definitions_['import_i2c'] = 'from machine import Pin';
    Blockly.Python.definitions_['import_mq3'] = 'from mq3 import MQ3';
    Blockly.Python.definitions_["import_create_mq3"] = 'mq3 = MQ3(Pin(' + dropdown_name + '.adc_pin)) # analog PIN';
    // TODO: Assemble Python into code variable.
    var code = 'mq3.get_acohol()';
    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Blockly.Python.ORDER_NONE];
  };

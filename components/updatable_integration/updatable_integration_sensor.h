#pragma once

#include "esphome/components/integration/integration_sensor.h"
#include "esphome/core/automation.h"

namespace esphome {
namespace updatable_integration {

class UpdatableIntegrationSensor : public integration::IntegrationSensor {
public:
    void set_value(float value) {
        this->last_value_ = value;
        this->last_update_ = millis();
        this->publish_and_save_(value);
    }
};


template<typename... Ts> class SetValueAction : public Action<Ts...> {
 public:
  SetValueAction(UpdatableIntegrationSensor *parent) : parent_(parent) {}
  TEMPLATABLE_VALUE(float, value);

  void play(Ts... x) {
    float val = this->value_.value(x...);
    this->parent_->set_value(val);
  }

  UpdatableIntegrationSensor *parent_;
};

} //namespace updatable_integration
} //namespace esphome
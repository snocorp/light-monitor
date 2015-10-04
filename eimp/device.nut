photosensor <- hardware.pin2;   // photo sensor pin
onlineLed <- hardware.pin5;     // device is online

photosensor.configure(ANALOG_IN);
onlineLed.configure(DIGITAL_OUT);

onlineLed.write(1);

function blink() {
    onlineLed.write(0);

    imp.wakeup(0.5, function() {
        onlineLed.write(1);
    });
}

function getSensorData(val) {
    blink();

    local values = {};
    values.light <- photosensor.read();
    agent.send("onSensorData", values);
}

// Register a handler for incoming messages from the agent
agent.on("requestSensorData", getSensorData);

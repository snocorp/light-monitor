// Log the URLs we need
server.log("Request light data: " + http.agenturl());

function requestSensorData(request, response) {
    try {
        device.send("requestSensorData", 0);

        device.on("onSensorData", function(val) {
            try {
                server.log("Light Sensor: " + val.light);
                response.send(200, "{\"light\": \"" + val.light + "\"}");
            } catch (ex1) {
                response.send(500, "{\"error\": \"Internal Server Error: " + ex1 + "\"}");
            }
        });
    } catch (ex) {
        response.send(500, "{\"error\": \"Internal Server Error: " + ex + "\"}");
    }
}

// Register the HTTP handler to begin watching for HTTP requests from your browser
http.onrequest(requestSensorData);

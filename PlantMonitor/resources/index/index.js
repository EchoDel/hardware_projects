fetch('/get_status')
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        console.log(data)
        update_data(data);
    })
    .catch(function (err) {
        console.log('error: ' + err);
    });

function update_data(data) {
    // update the ranges
    document.getElementById("soil_moisture_minimum").innerHTML = data.config.soil_moisture.minimum;
    document.getElementById("soil_moisture_maximum").innerHTML = data.config.soil_moisture.maximum;
    document.getElementById("soil_minimum").value = data.config.soil_moisture.minimum;
    document.getElementById("soil_maximum").value = data.config.soil_moisture.maximum;
    document.getElementById("air").value = data.config.soil_moisture_calibration.air;
    document.getElementById("water").value = data.config.soil_moisture_calibration.water;
    document.getElementById("current").innerHTML = 'Current ADC: ' + data.debug.adc_raw;

    document.getElementById("temperature_minimum").innerHTML = data.config.temperature.minimum;
    document.getElementById("temperature_maximum").innerHTML = data.config.temperature.maximum;
    document.getElementById("temp_minimum").value = data.config.temperature.minimum;
    document.getElementById("temp_maximum").value = data.config.temperature.maximum;

    // actual values
    var soil_value = document.getElementById("soil_value");
    soil_value.innerHTML = 'Soil Moisture : ' + data.soil_moisture
    var temperature_value = document.getElementById("temperature_value");
    temperature_value.innerHTML = 'Temperature : ' + data.temperature

    update_colours(data.soil_moisture, data.config.soil_moisture.minimum,
                   data.config.soil_moisture.maximum, "soil_moisture_box")

    update_colours(data.temperature, data.config.temperature.minimum,
                   data.config.temperature.maximum, "temperature_box")
}

red = '#FF7472'
amber = '#FFBF72'
green = '#72FFAF'

function update_colours(current, min, max, object_id){
    current_object = document.getElementById(object_id)
    if (current < min){
        current_object.style.backgroundColor = red
    } else if (current < min + 1) {
        current_object.style.backgroundColor = amber
    } else if (current < max - 1) {
        current_object.style.backgroundColor = green
    } else if (current < max) {
        current_object.style.backgroundColor = amber
    } else {
        current_object.style.backgroundColor = red
    }
}
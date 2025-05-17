function rebootPi1(command) {
    // Send a request to reboot the Raspberry Pi
    // You can use JavaScript's Fetch API or any other method to send the request
    // For example, you can use fetch('/reboot') if you have a server endpoint set up to handle reboots
    // Replace '/reboot' with the actual endpoint URL if needed
    fetch('http://192.168.1.144:5000/control/reboot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command }),
    })
    .then(response => {
            // Check if the request was successful
        if (!response.ok) {
            throw new Error('Failed to reboot the Raspberry Pi');
        }
        // Optional: Display a success message or perform any other actions if needed
        alert('Raspberry Pi is rebooting...');
        })
        .catch(error => {
            // Handle errors, e.g., display an error message to the user
            console.error('Error rebooting Raspberry Pi:', error);
            alert('Raspberry Pi is rebooting...');
        });
}

function rebootPi2(command) {
    // Send a request to reboot the Raspberry Pi
    // You can use JavaScript's Fetch API or any other method to send the request
    // For example, you can use fetch('/reboot') if you have a server endpoint set up to handle reboots
    // Replace '/reboot' with the actual endpoint URL if needed
    fetch('http://192.168.1.82:5000/control/reboot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command }),
    })
    .then(response => {
            // Check if the request was successful
        if (!response.ok) {
            throw new Error('Failed to reboot the Raspberry Pi');
        }
        // Optional: Display a success message or perform any other actions if needed
        alert('Raspberry Pi is rebooting...');
        })
        .catch(error => {
            // Handle errors, e.g., display an error message to the user
            console.error('Error rebooting Raspberry Pi:', error);
            alert('Raspberry Pi is rebooting...');
        });
}

// Function to send control commands for lights
function controlLights(command) {
    fetch('http://192.168.1.144:5000/control/lights', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command }),
    })
    .then(response => response.json())
    .then(data => {
        // Update lights status
        const statusLights = document.getElementById('status-lights');
        statusLights.textContent = data.light_status ? 'On' : 'Off';
    })
    .catch(error => {
        console.error('Error sending command:', error);
    });
}

// Function to send control commands for the heater
function controlHeater(command) {
    fetch('http://192.168.1.144:5000/control/heater', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command }),
    })
    .then(response => response.json())
    .then(data => {
        // Update heater status
        const statusHeater = document.getElementById('status-heater');
        statusHeater.textContent = data.heater_status ? 'On' : 'Off';
    })
    .catch(error => {
        console.error('Error sending command:', error);
    });
}

function controlCabinetLights(command) {
    fetch('http://192.168.1.144:5000/control/cabinetlights', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command }),
    })
    .then(response => response.json())
    .then(data => {
        // Update cabinet lights status
        const statusCabinetLights = document.getElementById('status-cabinet-lights');
        statusCabinetLights.textContent = data.cabinet_lights_status ? 'On' : 'Off';
    })
    .catch(error => {
        console.error('Error sending command:', error);
    });
}

function controlPump(command) {
    fetch('http://192.168.1.144:5000/control/pump', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Pump on/off sent');
        // Update cabinet lights status
        // const statusCabinetLights = document.getElementById('status-cabinet-lights');
        // statusCabinetLights.textContent = data.cabinet_lights_status ? 'On' : 'Off';
    })
    .catch(error => {
        console.error('Error sending command:', error);
    });
}

// Function to set the lights' turn-on time
function setLightsOnTime() {
    const lightsOnTimeInput = document.getElementById('lights-on-time');
    const newTime = lightsOnTimeInput.value;

    // Send the new time to the server (you'll need to update the server code)
    fetch('http://192.168.1.144:5000/set/lights/on-time', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ lights_on_time: newTime }),
    })
    .then(response => response.json())
    .then(data => {
        // Update the displayed time if needed
        // For example, you can display a confirmation message
        console.log('Lights turn-on time updated:', data.lights_on_time);
    })
    .catch(error => {
        console.error('Error setting lights turn-on time:', error);
    });
}

// Function to set the lights' turn-off time
function setLightsOffTime() {
    const lightsOffTimeInput = document.getElementById('lights-off-time');
    const newTime = lightsOffTimeInput.value;

    // Send the new time to the server (you'll need to update the server code)
    fetch('http://192.168.1.144:5000/set/lights/off-time', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ lights_off_time: newTime }),
    })
    .then(response => response.json())
    .then(data => {
        // Update the displayed time if needed
        // For example, you can display a confirmation message
        console.log('Lights turn-off time updated:', data.lights_off_time);
    })
    .catch(error => {
        console.error('Error setting lights turn-off time:', error);
    });
}

// Function to set the heater-on temperature
function setHeaterOnTemp() {
    const heaterOnTempInput = document.getElementById('heater-on-temp');
    const newTemp = heaterOnTempInput.value;

    // Send the new temperature to the server (you'll need to update the server code)
    fetch('http://192.168.1.144:5000/set/heater/on-temp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ heater_on_temp: newTemp }),
    })
    .then(response => response.json())
    .then(data => {
        // Update the displayed temperature if needed
        // For example, you can display a confirmation message
        console.log('Heater-on temperature updated:', data.heater_on_temp);
    })
    .catch(error => {
        console.error('Error setting heater-on temperature:', error);
    });
}

// Function to set the heater-off temperature
function setHeaterOffTemp() {
    const heaterOffTempInput = document.getElementById('heater-off-temp');
    const newTemp = heaterOffTempInput.value;

    // Send the new temperature to the server (you'll need to update the server code)
    fetch('http://192.168.1.144:5000/set/heater/off-temp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ heater_off_temp: newTemp }),
    })
    .then(response => response.json())
    .then(data => {
        // Update the displayed temperature if needed
        // For example, you can display a confirmation message
        console.log('Heater-off temperature updated:', data.heater_off_temp);
    })
    .catch(error => {
        console.error('Error setting heater-off temperature:', error);
    });
}

// Function to fetch and update status
function updateStatus() {
    fetch('http://192.168.1.144:5000/status')
        .then(response => response.json())
        .then(data => {
            // Update status indicators on the website

            const statusLights = document.getElementById('status-lights');
            const statusHeater = document.getElementById('status-heater');
            const statusPump = document.getElementById('status-pump');
            const statusCabinetLights = document.getElementById('status-cabinet-lights');
            const waterTemperature = document.getElementById('water-temperature');
            const currentDatetime = document.getElementById('current-datetime');

            const pi1Status = document.getElementById('pi1-status');
            pi1Status.textContent = data.pi1StatusIndicator;
            pi1Status.style.color = "#00ff00";

            const lightsOnTime = document.getElementById('lights-on-time');
            const lightsOffTime = document.getElementById('lights-off-time');

            const heaterOnTemp = document.getElementById('heater-on-temp');
            const heaterOffTemp = document.getElementById('heater-off-temp');

            const intTime = data.int_time;

            const systemUptime = document.getElementById('system-uptime');

            statusPump.textContent = data.pump_status ? 'On' : 'Off';
            statusLights.textContent = data.light_status ? 'On' : 'Off';
            statusHeater.textContent = data.heater_status ? 'On' : 'Off';
            statusCabinetLights.textContent = data.cabinet_lights_status ? 'On' : 'Off';

            waterTemperature.textContent = data.water_temperature + 'Â°C';
            currentDatetime.textContent = data.current_datetime;
            systemUptime.textContent = data.system_uptime + " ";

            lightsOnTime.value = data.lights_on_time;
            lightsOffTime.value = data.lights_off_time;

            heaterOnTemp.value = data.heater_on_temp;
            heaterOffTemp.value = data.heater_off_temp;

            if (data.pump_status === true) {
                const pumpElement = document.getElementById('status-pump');
                pumpElement.classList.remove('on', 'off');
                pumpElement.classList.add('on');
            } else {
                const pumpElement = document.getElementById('status-pump');
                pumpElement.classList.remove('on', 'off');
                pumpElement.classList.add('off');
            }
            const lightElement = document.getElementById('status-lights');
            lightElement.classList.remove('on', 'off', 'auto-on', 'auto-off');

            if (data.lights_forced === 1) {
                lightElement.classList.add('on');
                lightElement.innerText = 'On';
            } else if (data.lights_forced === 2) {
                lightElement.classList.add('off');
                lightElement.innerText = 'Off';
            } else {
                if (data.light_status === true) {
                lightElement.classList.add('auto-on');
                lightElement.innerText = 'Auto On';
                } else {
                lightElement.classList.add('auto-off');
                lightElement.innerText = 'Auto Off';
                }
            }

            const heaterElement = document.getElementById('status-heater');
            heaterElement.classList.remove('on', 'off', 'auto-on', 'auto-off');

            if (data.heater_forced === 1) {
            heaterElement.classList.add('on');
            heaterElement.innerText = 'On';
            } else if (data.heater_forced === 2) {
            heaterElement.classList.add('off');
            heaterElement.innerText = 'Off';
            } else {
                if (data.heater_status === true) {
                heaterElement.classList.add('auto-on');
                heaterElement.innerText = 'Auto On';
                } else {
                heaterElement.classList.add('auto-off');
                heaterElement.innerText = 'Auto Off';
                }
            }

            if (data.cabinet_lights_status === true) {
                const cabinetLightsElement = document.getElementById('status-cabinet-lights');
                cabinetLightsElement.classList.remove('on', 'off');
                cabinetLightsElement.classList.add('on');
            } else {
                const cabinetLightsElement = document.getElementById('status-cabinet-lights');
                cabinetLightsElement.classList.remove('on', 'off');
                cabinetLightsElement.classList.add('off');
            }


        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });

}
// Function to fetch and update status
function updateStatusGoldFish() {
    fetch('http://192.168.1.82:5000/status')
        .then(response => response.json())
        .then(data => {
            const pi2Status = document.getElementById('pi2-status');
            pi2Status.textContent = data.pi2StatusIndicator;
            pi2Status.style.color = "#00ff00";

            const waterTemperatureGoldfish = document.getElementById('water-temperature-goldfish');
            waterTemperatureGoldfish.textContent = data.water_temperature_goldfish + 'Â°C';

            const systemUptimeGoldFish = document.getElementById('system-uptime-goldfish');
            systemUptimeGoldFish.textContent = data.system_uptime_goldfish + " ";

        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });

}

// Call updateStatus initially and every 5 seconds
updateStatus();
setInterval(updateStatus, 2000);
setInterval(updateStatusGoldFish, 2000);

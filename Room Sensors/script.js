function rebootPi(command) {
    // Send a request to reboot the Raspberry Pi
    // You can use JavaScript's Fetch API or any other method to send the request
    // For example, you can use fetch('/reboot') if you have a server endpoint set up to handle reboots
    // Replace '/reboot' with the actual endpoint URL if needed
    fetch('http://192.168.1.249:5000/control/reboot', {
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


// Function to fetch and update status
function updateStatus() {
    fetch('http://localhost:5000/sensor')
        .then(response => response.json())
        .then(data => {


            const roomTemp = document.getElementById('temp-2');
            roomTemp.textContent = data.temperature + '°C';
            // Update status indicators on the website

            const roomHumidity = document.getElementById('humidity-2');
            roomHumidity.textContent = data.humidity + '%';
            // Update status indicators on the website

        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });

} 


// Call updateStatus initially and every 5 seconds
updateStatus();
setInterval(updateStatus, 5000);

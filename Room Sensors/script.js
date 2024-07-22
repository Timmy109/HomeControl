    // Function to fetch data from the server and update the DOM
    function fetchData() {
        fetch('http://192.168.1.125:5000/data')
            .then(response => response.json())
            .then(data => {
                for (let ip in data) {
                    var roomDiv = document.getElementById(ip);
                    if (roomDiv) {
                        roomDiv.querySelector('.temperature').innerText = Math.round((data[ip].temperature - 3) * 10) / 10 + "Â°C";
                        roomDiv.querySelector('.humidity').innerText = data[ip].humidity + "%";
                        roomDiv.querySelector('.status').innerText = "â¦¿ Online";
                        roomDiv.querySelector('.status').style.color = "green";
                        roomDiv.dataset.lastSeen = Date.now();
                        console.log(`Fetched ${ip}: ${roomDiv.dataset.lastSeen}`);  // Debug statement
                    }
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Function to fetch server uptime and update the DOM
    function fetchUptime() {
        fetch('http://192.168.1.125:5000/uptime')
            .then(response => response.json())
            .then(data => {
                document.getElementById('system-uptime').innerText = data.uptime;
            })
            .catch(error => console.error('Error fetching uptime:', error));
    }

    // Fetch data and uptime periodically
    setInterval(fetchData, 5000); // Every 5 seconds
    setInterval(fetchUptime, 10000); // Every 10 seconds

    // Initial fetch
    fetchData();
    fetchUptime();

let chart; // Declares global chart instance
// Defines function for timestamp.
function formatTimestamp(rawTime) {
    const date = new Date(rawTime); // Create date object.
    const day = date.getDate(); // Retrieves date.
    // Gets day suffix (st, nd, rd, th).
    const daySuffix = d => {
        if (d > 3 && d < 21) return 'th';
        const suffixes = ['th', 'st', 'nd', 'rd'];
        return suffixes[d % 10] || 'th';};
    // Format month and time (24hr clock).
    const optionsDate = { month: 'short' };
    const optionsTime = { hour: '2-digit', minute: '2-digit', hour12: false };
    const month = date.toLocaleString('en-US', optionsDate); // Gets month.
    const time = date.toLocaleTimeString('en-US', optionsTime); // Gets time.
    // Returns date in readable sting.
    return `${month} ${day}${daySuffix(day)} ${time}`;
}
// function for generating and updating chart.
function Generate_Update_Chart(ctx, labels, temps, pointColors) {
    Chart.defaults.font.family = 'Libre Baskerville, serif'; // Global default font style.
    Chart.defaults.font.size = 14; // Global default font size.
    Chart.defaults.color = '#222'; // Global default font color.
    // Creates a chart if none present.
    if (!chart) {
        chart = new Chart(ctx, {
            // Creates a line chart with style information.
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Avg Temp (°F)',
                    data: temps,
                    borderColor: '#444',
                    backgroundColor: 'transparent',
                    pointBorderColor: pointColors,
                    pointBackgroundColor: pointColors,
                    tension: 0.3,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 10,
                    pointHitRadius: 15
                }]
            },
            // Defines options for responsive interactions and axis.
            options: {
                responsive: true,
                interaction: {mode: 'index', intersect: false},
                hover: {mode: 'index', intersect: false},
                scales: {
                    y: { 
                        min: 0, 
                        max: 120, 
                        title: {display: true, text: 'Temperature (°F)'}
                    },
                    x: {
                        title: {display: true, text: 'Timestamp'},
                        ticks: {maxRotation: 0, minRotation: 0, font: {size: 10}}
                    }
                }
            }
        });
    } 
    // Updates the chart if generated.
    else {
    // Updates new data & labels
    chart.data.labels = labels;
    chart.data.datasets[0].data = temps;
    chart.data.datasets[0].pointBackgroundColor = pointColors;
     // Creates gradient fill for temp range.
    const gradient = ctx.createLinearGradient(0, chart.chartArea.top, 0, chart.chartArea.bottom);
    const getStop = temp => 1 - (temp / 120);
    // Gradient styling to visualize temperature ranges.
    gradient.addColorStop(getStop(120), 'transparent');
    gradient.addColorStop(getStop(120), 'red');
    gradient.addColorStop(getStop(100), 'red');
    gradient.addColorStop(getStop(95), 'green');
    gradient.addColorStop(getStop(25), 'green');
    gradient.addColorStop(getStop(20), 'blue');
    gradient.addColorStop(getStop(0), 'blue');
    chart.data.datasets[0].backgroundColor = gradient;
    chart.update();
    }
    chart.render();
}
// Fetches temperature data, formats labels, sets point colors, updates the chart, and displays the last update time.
function loadDataAndUpdateChart() {
    fetch('avgTemps.json?v=' + Date.now()) // Fetch temperature JSON data
        .then(response => {
            if (!response.ok) throw new Error('Could not load avgTemps.json'); // Check if response is OK
            return response.json(); // Parse JSON
        })
        .then(data => {
            // Prepare labels: show for first, last, and every other point
            const labels = data.map((entry, index) => {
                const isFirst = index === 0;
                const isLast = index === data.length - 1;
                const isEven = index % 2 === 0;
                return (isFirst || isLast || isEven) ? formatTimestamp(entry.time) : '';
            });
            // Extract temperatures
            const temps = data.map(entry => entry.avgTemp);
            // Assign point colors based on temperature range.
            const pointColors = temps.map(temp => {
                if (temp < 25) return 'blue';
                if (temp > 100) return 'red';
                return 'green';
            });
             // Get canvas context
            const ctx = document.getElementById('tempChart').getContext('2d');
            // Calls update chart function.
            Generate_Update_Chart(ctx, labels, temps, pointColors);
            // Update the "last updated" time
            const now = new Date();
            document.getElementById('lastUpdated').textContent =
                `Last updated: ${now.toLocaleTimeString()}`;
        })
        .catch(err => {console.error('Error loading temperature data.', err);});
}
// Load data immediately, then refresh every 1000 milliseconds.
loadDataAndUpdateChart();
setInterval(loadDataAndUpdateChart, 1_000);
function renderChart(chartData) {
    const ctx = document.getElementById('bmiChart').getContext('2d');

    new Chart(ctx, {
        type: 'doughnut',  // Change to pie or doughnut
        data: {
            labels: chartData.labels,   // ["Underweight", "Normal", "Overweight", "Obesity"]
            datasets: [{
                label: "BMI Categories",
                data: chartData.ranges, // [18.5, 24.9, 29.9, 40]
                backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545'],
                hoverOffset: 8
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                title: {
                    display: true,
                    text: `Your BMI: ${chartData.user_bmi}`
                }
            }
        }
    });
}

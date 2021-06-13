// charts
var ramChart = new Chart(
    document.querySelector('div#ram-usage canvas.stat').getContext('2d'),
    {
        type: 'line',
        data: {
            labels: ['', '', '', '', '', '', ''],
            datasets: [{
                label: 'RAM Usage (%)',
                backgroundColor: 'rgba(55, 168, 67, .2)',
                pointBackgroundColor: '#37a843',
                borderColor: '#37a843',
                borderWidth: 1,
                color: '#fff',
                pointRadius: 0,
                cubicInterpolationMode: 'monotone',
                pointHoverRadius: 2,
                data: [0, 10, 5, 2, 20, 30, 45],
                fill: {
                    target: 'origin',
                    below: 'rgba(55, 168, 67, .2)'
                }
            }]
        },
        options: {
            scales: {
                y: {
                    stacked: true,
                    grid: {
                        color: '#fff'
                    },
                    labels: {
                        color: '#fff'
                    }
                },
                x: {
                    grid: {
                        color: '#fff'
                    }
                }
            }
        }
    }
);

var cpuChart = new Chart(
    document.querySelector('div#cpu canvas.stat').getContext('2d'),
    {
        type: 'line',
        data: {
            labels: ['', '', '', '', '', '', ''],
            datasets: [{
                label: 'CPU Usage (%)',
                backgroundColor: '#37a843',
                borderColor: '#37a843',
                data: [0, 10, 5, 2, 20, 30, 45],
            }]
        },
        options: {}
    }
);

// fetch content
const fetchHistory = [];
let currentFetch = {};

var fetchInt = setInterval(() => {
    axios.post('http://50.255.24.101:2001/', {
        SysName: 'NES', 
        CallStack:'LFTM.SystemTelemetryManager.mAPI_GetAllNodeStats',
        KeywordArgs: {}
    }).then(function (response) {
        // handle success
        fetchHistory.push(response.data);
        currentFetch = response.data;
        let nodeList = '';
        for (var n in currentFetch.Content) {
            nodeList += '<li>' + n + '</li>';
            if (currentFetch 
                && currentFetch.Content 
                && currentFetch.Content[n] 
                && currentFetch.Content[n].RAMUsage) {
                document.querySelector('#ram-usage span').innerText = currentFetch.Content[n].RAMUsage;
            }
        }
        if (!!nodeList) {
            document.querySelector('#node-list').innerHTML = nodeList;
        }
    })
    .catch(function (error) {
        // handle error
        console.log(error);
    });
}, 1000);
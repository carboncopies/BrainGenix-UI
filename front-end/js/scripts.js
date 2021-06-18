// charts
var ramChart = new Chart(
    document.querySelector("div#ram-usage canvas.stat").getContext("2d"),
    {
        type: "line",
        data: {
            labels: ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            datasets: [{
                label: "",
                backgroundColor: "rgba(55, 168, 67, .2)",
                pointBackgroundColor: "#37a843",
                borderColor: "#37a843",
                borderWidth: 1,
                color: "#fff",
                pointRadius: 0,
                cubicInterpolationMode: "monotone",
                pointHoverRadius: 2,
                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                fill: {
                    target: "origin",
                    below: "rgba(55, 168, 67, .2)"
                }
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                y: {
                    stacked: true,
                    grid: {
                        color: "rgba(255, 255, 255, .2)"
                    },
                    gridLines: {
                        display: false
                    },
                    min: 0,
                    max: 100
                },
                x: {
                    grid: {
                        color: "transparent"
                    }
                }
            },
            animation: {
                duration: 0 // general animation time
            },
            hover: {
                animationDuration: 0 // duration of animations when hovering an item
            },
            responsiveAnimationDuration: 0, // animation duration after a resize
            elements: {
                line: {
                    tension: 0 // disables bezier curves
                }
            }
        }
    }
);

var cpuChart = new Chart(
    document.querySelector("div#cpu canvas.stat").getContext("2d"),
    {
        type: "line",
        data: {
            labels: ["", "", "", "", "", "", "", "", "", ""],
            datasets: [{
                max: 100,
                label: "CPU Usage (%)",
                backgroundColor: "rgba(55, 168, 67, .2)",
                pointBackgroundColor: "#37a843",
                borderColor: "#37a843",
                borderWidth: 1,
                color: "#fff",
                pointRadius: 0,
                // cubicInterpolationMode: "monotone",
                pointHoverRadius: 2,
                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                fill: {
                    target: "origin",
                    below: "rgba(55, 168, 67, .2)"
                }
            }]
        },
        options: {
            scales: {
                y: {
                    stacked: true,
                    grid: {
                        color: "transparent"
                    },
                    min: 0,
                    max: 100
                },
                x: {
                    grid: {
                        color: "transparent"
                    }
                }
            },
            animation: {
                duration: 0 // general animation time
            },
            hover: {
                animationDuration: 0 // duration of animations when hovering an item
            },
            responsiveAnimationDuration: 0, // animation duration after a resize
            elements: {
                line: {
                    tension: 0 // disables bezier curves
                }
            }
        }
    }
);

// fetch content
const fetchHistory = [];
let currentFetch = {};

var fetchInt = setInterval(() => {
    axios.post("http://50.255.24.101:2001/", {
        SysName: "NES", 
        CallStack:"LFTM.SystemTelemetryManager.mAPI_GetAllNodeStats",
        KeywordArgs: {}
    }).then(function (response) {
        // handle success
        fetchHistory.push(response.data);
        currentFetch = response.data;
        let nodeList = "";
        for (var n in currentFetch.Content) {
            nodeList += "<li>" + n + "</li>";
            if (currentFetch 
                && currentFetch.Content 
                && currentFetch.Content[n] 
                && currentFetch.Content[n].RAMUsage) {
                document.querySelector("span#ru-stats").innerText = currentFetch.Content[n].RAMPercent + "% | " + currentFetch.Content[n].RAMUsage;
                ramChart.data.datasets[0].data.push(currentFetch.Content[n].RAMPercent);
                if (ramChart.data.datasets[0].data.length > 20) {
                    ramChart.data.datasets[0].data.shift();
                }
                ramChart.update();
            }
        }
        if (!!nodeList) {
            document.querySelector("#node-list").innerHTML = nodeList;
        }
    })
    .catch(function (error) {
        clearInterval(fetchInt);
        notify("The API server cannot be reached!", "error");
    });
}, 75);

// notifications 
function notify(message, status) {
    let el = document.querySelector("div.notification"),
        t = '<h2>Error</h2>',
        b = '<div class="close-notification" onclick="notify();"><span class="iconify" data-icon="ion-close-circle-outline"></span></div>';
    if (!message || message === 'quit') {
        el.classList.remove('active'); 
        return;
    }
    switch(status) {
        case 'log':
            t = '<h2 class="notify-log">Log</h2>';
            break;
        case 'error':
            t = '<h2 class="notify-error">Error</h2>';
            break;
        case 'success':
            t = '<h2 class="notify-success">Success!</h2>';
            break;
    }
    el.innerHTML = b + t + '<p>' + message + '</p>';
    el.classList.add('active');
}

document.querySelector('div.close-notification').addEventListener('click', () => { notify(); });

// router and navigation 
function navigate(page) {
    let pgs = document.querySelectorAll('.pg');
    pgs.forEach(pg => {
        pg.classList.remove('active');
    });
    document.querySelector('#' + page).classList.add('active');
    if (page === 'Terminal') {
        // terminal 
        var term = new Terminal();
        var fitAddon = new FitAddon.FitAddon();
        term.loadAddon(fitAddon);
        term.open(document.getElementById('terminal'));
        term.write('BrainGenix-UI $ ');
        window.term = term;
        window.fitAddon = fitAddon;
        setTimeout(() => { fitAddon.fit(); }, 250);
    }
}
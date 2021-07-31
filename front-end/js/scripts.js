// charts
var ramChart = new Chart(
    document.querySelector('div#ram-usage canvas.stat').getContext('2d'), {
        type: 'line',
        data: {
            labels: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            datasets: [{
                label: '',
                backgroundColor: 'rgba(55, 168, 67, .2)',
                pointBackgroundColor: '#37a843',
                borderColor: '#37a843',
                borderWidth: 1,
                color: '#fff',
                pointRadius: 0,
                cubicInterpolationMode: 'monotone',
                pointHoverRadius: 2,
                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                // fill: {
                //     target: 'origin',
                //     below: 'rgba(55, 168, 67, .2)'
                // }
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
                        color: 'rgba(255, 255, 255, .2)'
                    },
                    gridLines: {
                        display: false
                    },
                    min: 0,
                    max: 100
                },
                x: {
                    grid: {
                        color: 'transparent'
                    }
                }
            },
            animation: {
                duration: 250 // general animation time
            },
            hover: {
                animationDuration: 0 // duration of animations when hovering an item
            },
            responsiveAnimationDuration: 200, // animation duration after a resize
            elements: {
                line: {
                    tension: 0 // disables bezier curves
                }
            }
        }
    }
);

var cpuChart = new Chart(
    document.querySelector('div#cpu canvas.stat').getContext('2d'), {
        type: 'line',
        data: {
            labels: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            datasets: [{
                label: '',
                backgroundColor: 'rgba(55, 168, 67, .2)',
                pointBackgroundColor: '#37a843',
                borderColor: '#37a843',
                borderWidth: 1,
                color: '#fff',
                pointRadius: 0,
                cubicInterpolationMode: 'monotone',
                pointHoverRadius: 2,
                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                // fill: {
                //     target: 'origin',
                //     below: 'rgba(55, 168, 67, .2)'
                // }
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
                        color: 'rgba(255, 255, 255, .2)'
                    },
                    gridLines: {
                        display: false
                    },
                    min: 0,
                    max: 100
                },
                x: {
                    grid: {
                        color: 'transparent'
                    }
                }
            },
            animation: {
                duration: 250 // general animation time
            },
            hover: {
                animationDuration: 0 // duration of animations when hovering an item
            },
            responsiveAnimationDuration: 200, // animation duration after a resize
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
let fetchInt;
let fetchRate = 1000;
const totalAv = function(arr) {
    let total = 0;
    arr.forEach(item => {
        total += item;
    });
    return Number.parseFloat(total / arr.length).toFixed(2);
};
let activeNodes = [];

var fetchData = (cmd) => {
    if (!!window.localStorage.bgxToken) {
        axios.post(apiRoute, {
                Token: window.localStorage.bgxToken,
                SysName: 'NES',
                CallStack: 'LFTM.SystemTelemetryManager.GetAllNodeStats',
                KeywordArgs: {}
            }).then(function(response) {
                // handle success
                if (cmd === 'init' && response.data && response.data.Content !== "Expired Token") {
                    toggleLoginModal();
                    fetchInt = setInterval(() => {
                        fetchData();
                    }, fetchRate);
                }
                fetchHistory.push(response.data);
                currentFetch = response.data;
                if (response.data.Name === "Error" && response.data.Content !== "Expired Token") {
                    if (cmd !== 'init') {
                        notify(response.data.Content, 'error');
                    }
                    clearInterval(fetchInt);
                    return;
                }
                if (response.data.Name === "Error" && response.data.Content === "Expired Token") {
                    toggleLoginModal();
                    clearInterval(fetchInt);
                }
                let nodeList = '',
                    ramArr = [],
                    cpuArr = [],
                    ramAv = 0,
                    cpuAv = 0;
                for (var n in currentFetch.Content) {
                    if (!activeNodes.includes(n) && !Number(n)) {
                        activeNodes.push(n);
                        nodeList += '<li>' + n + '</li>';
                    }
                    // add ram 
                    if (currentFetch &&
                        currentFetch.Content &&
                        currentFetch.Content[n] &&
                        currentFetch.Content[n].RAMUsage) {
                        ramArr.push(currentFetch.Content[n].RAMPercent);
                    }
                    if (currentFetch &&
                        currentFetch.Content &&
                        currentFetch.Content[n] &&
                        currentFetch.Content[n].CPUUsage) {
                        cpuArr.push(...currentFetch.Content[n].CPUUsage);
                    }
                }
                // update chart and html with averaged ram data
                ramChart.data.datasets[0].data.push(totalAv(ramArr));
                if (ramChart.data.datasets[0].data.length > 20) {
                    ramChart.data.datasets[0].data.shift();
                }
                ramChart.update();
                document.querySelector('span#ru-stats').innerText = totalAv(ramArr) + '%';
                // update chart and html with averaged cpu data
                cpuChart.data.datasets[0].data.push(totalAv(cpuArr));
                if (cpuChart.data.datasets[0].data.length > 20) {
                    cpuChart.data.datasets[0].data.shift();
                }
                cpuChart.update();
                document.querySelector('span#cu-stats').innerText = totalAv(cpuArr) + '%';
                if (nodeList !== '') {
                    if (document.querySelector('#node-list').innerText === 'Loading...') {
                        document.querySelector('#node-list').innerHTML = nodeList
                    } else {
                        document.querySelector('#node-list').innerHTML += nodeList;
                    }
                }
                document.querySelector('#total-nodes').innerText = activeNodes.length;
            })
            .catch(function(error) {
                notify('API connection error!', 'error');
                console.log(error);
            });
    }
}

// notifications 
function notify(message, status) {
    let el = document.querySelector('div.notification'),
        t = '<h2>Error</h2>',
        b = '<div class="close-notification" onclick="notify();"><span class="iconify" data-icon="ion-close-circle-outline"></span></div>';
    if (!message || message === 'quit') {
        el.classList.remove('active');
        return;
    }
    switch (status) {
        case 'log':
            t = '<h2 class="notify-log">Log</h2>';
            break;
        case 'error':
            t = '<h2 class="notify-error">Error</h2>';
            break;
        case 'success':
            t = '<h2 class="notify-success">Success!</h2>';
            break;
        case 'info':
            t = '<h2 class="notify-info">Info...</h2>';
            break;
    }
    el.innerHTML = b + t + '<p>' + message + '</p>';
    el.classList.add('active');
}

document.querySelector('div.close-notification').addEventListener('click', () => { notify(); });

// router and navigation 
function navigate(page) {
    if (!!document.querySelector('#' + page.replace(/ /gi, '-'))) {
        let pgs = document.querySelectorAll('.pg');
        pgs.forEach(pg => {
            pg.classList.remove('active');
        });
        document.querySelector('#' + page.replace(/ /gi, '-')).classList.add('active');
        window.location.hash = '#' + page.replace(/ /gi, '-').toLowerCase();
    }
}
if (window.location.pathname === '/') {
    navigate('Dashboard');
}

function login() {
    document.querySelector('#login-button').classList.add('is-loading');
    axios.post(apiRoute + 'Authenticate', {
        Username: document.querySelector('#username').value,
        Password: document.querySelector('#password').value
    }).then(response => {
        if (response.data && response.data.Token) {
            document.querySelector('#login-button').classList.remove('is-loading');
            document.querySelector('#login-modal').classList.remove('is-active');
            window.localStorage.setItem('bgxToken', response.data.Token);
            if (fetchInt) {
                clearInterval(fetchInt);
            }
            fetchInt = setInterval(() => {
                fetchData();
            }, fetchRate);
            fetchData();
        }
    }).catch(err => {
        console.log(err);
    });
}

function toggleLoginModal() {
    var loginModal = document.querySelector('#login-modal');
    if (!loginModal.classList.contains('is-active')) {
        loginModal.classList.add('is-active');
        document.querySelector('#username').focus();
    } else {
        loginModal.classList.remove('is-active');
    }
}

// upon page load JS determines if a bgxToken exists
if (window.localStorage.bgxToken) {
    // if so an attempt to fetch data is made:
    fetchData('init');
}

// when li with class 'submenu' is clicked toggle class 'open'
document.querySelectorAll('.submenu').forEach(li => {
    li.addEventListener('click', (e) => {
        e.currentTarget.classList.toggle('open');
        e.cancelBubble = true;
    });
});

// when li span is clicked cancel bubbling
document.querySelectorAll('li:not(.submenu) > span').forEach(sp => {
    sp.addEventListener('click', (e) => {
        navigate(e.currentTarget.innerText);
        e.cancelBubble = true;
    });
});

let terminalPrintHistory = [];

function terminalPrint(message, type, noHistory) {
    // types: 'log', 'error', 'success', 'info', 'warn'
    if (!type) {
        type = 'log';
    }
    let el = document.querySelector('#terminal-logs');
    let msg = document.createElement('pre');
    msg.classList.add(type);
    msg.innerHTML = message;
    el.append(msg);
    if (!noHistory) {
        terminalPrintHistory.push({
            message: message,
            type: type,
            time: new Date().getTime()
        });
    }
}

// when you press enter and #terminal-input is focused execute function
document.querySelector('#terminal-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        var terminalInput = document.querySelector('#terminal-input').value;
        document.querySelector('#terminal-input').value = '';
        if (terminalInput === 'help' || terminalInput === '?' || terminalInput === 'h') {
            terminalPrint(`BrainGenix UI $ > Help is here! Try out some of the commands below:
help, h, ?            | brings up this message...
clear                 | clears the terminal screen (logs can be restored)
quit, q               | clears terminal logs and navigates to the Dashboard
restore logs, r -a    | brings back all recent logs`, 'log');
            return;
        }
        if (terminalInput === 'quit' || terminalInput === 'q') {
            terminalPrint('BrainGenix UI $ > Bye!', 'log');
            setTimeout(function() {
                document.querySelector('#terminal-logs').innerHTML = '';
                setTimeout(function() {
                    navigate('Dashboard');
                }, 1000);
            }, 1000);
            return;
        }
        if (terminalInput === 'restore logs' || terminalInput === 'r -a') {
            if (document.querySelector('#terminal-logs').innerHTML == '' && terminalPrintHistory.length > 0) {
                terminalPrintHistory.forEach(log => {
                    terminalPrint(log.message, log.type, true);
                });
            } else if (document.querySelector('#terminal-logs').innerHTML == '' && terminalPrintHistory.length === 0) {
                terminalPrint('BrainGenix UI $ > Oops, there are no logs to display!', 'warn');
            } else if (document.querySelector('#terminal-logs').innerHTML !== '') {
                terminalPrint('BrainGenix UI $ > You already have logs! Try \'clear\' to clear the logs, or \'quit\' to return to the Dashboard.', 'warn');
            }
            return;
        }
        if (terminalInput === 'clear') {
            document.querySelector('#terminal-logs').innerHTML = '';
            return;
        }
        if (terminalInput === 'login') {
            toggleLoginModal();
            return;
        }
        if (terminalInput === 'about') {
            terminalPrint('BrainGenix UI $ > This platform was built to access and work with other BrainGenix offerings. It is built using modern JavaScript, Node.js, Pug, Axios, and many other cool JS libraries.', 'log');
            return;
        }
        terminalPrint(`BrainGenix UI $ > Command \'${terminalInput}\' not recognized...`, 'error');
    }
});

function terminalFetch(cs) {
    if (!cs || cs === 'log') {
        cs = 'LFTM.Logger.CLAS.ReadLog';
    }
    // fire axios post request along with the token
    axios.post(apiRoute, {
        Token: window.localStorage.bgxToken,
        SysName: 'NES',
        CallStack: cs,
        KeywordArgs: {
            Lines: 50
        }
    }).then(response => {
        // if successful, append the response to the #terminal-logs element
        console.log(response);
    }).catch(error => {
        console.log(error);
    });
}
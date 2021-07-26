// charts
var ramChart = new Chart(
    document.querySelector('div#ram-usage canvas.stat').getContext('2d'),
    {
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
    document.querySelector('div#cpu canvas.stat').getContext('2d'),
    {
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
        axios.post('http://50.255.24.101:2001/', {
            Token: window.localStorage.bgxToken,
            SysName: 'NES', 
            CallStack:'LFTM.SystemTelemetryManager.GetAllNodeStats',
            KeywordArgs: {}
        }).then(function (response) {
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
                if (currentFetch 
                    && currentFetch.Content 
                    && currentFetch.Content[n] 
                    && currentFetch.Content[n].RAMUsage) {
                    ramArr.push(currentFetch.Content[n].RAMPercent);
                }
                if (currentFetch 
                    && currentFetch.Content 
                    && currentFetch.Content[n] 
                    && currentFetch.Content[n].CPUUsage) {
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
        .catch(function (error) {
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
        case 'info':
            t = '<h2 class="notify-info">Info...</h2>';
            break;
    }
    el.innerHTML = b + t + '<p>' + message + '</p>';
    el.classList.add('active');
}

document.querySelector('div.close-notification').addEventListener('click', () => { notify(); });

function loadLogTerm() {
    var logTerm = new Terminal();
    var fitAddonLog = new FitAddon.FitAddon();
    logTerm.loadAddon(fitAddonLog);
    logTerm.open(document.getElementById('log-term'));
    logTerm.write('BrainGenix-UI $ ');
    window.logTerm = logTerm;
    window.fitAddonLog = fitAddonLog;
    setTimeout(() => { fitAddonLog.fit(); }, 250);
}

function loadConsole() {
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
// router and navigation 
function navigate(page) {
    if (!!document.querySelector('#' + page.replace(/ /gi, '-'))) {
        let pgs = document.querySelectorAll('.pg');
        pgs.forEach(pg => {
            pg.classList.remove('active');
        });
        document.querySelector('#' + page.replace(/ /gi, '-')).classList.add('active');
        window.location.hash = '#' + page.replace(/ /gi, '-').toLowerCase();
        if (page === 'Console') {
            loadConsole();
        }
        if (page === 'Dashboard') {
            loadLogTerm();
        }
    }
}

function login() {
    document.querySelector('#login-button').classList.add('is-loading');
    axios.post('http://50.255.24.101:2001/Authenticate', {
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
    } else {
        loginModal.classList.remove('is-active');
    }
}

// upon page load JS determines if a bgxToken exists
if (window.localStorage.bgxToken) {
    // if so an attempt to fetch data is made:
    fetchData('init');
}

// upon page load if route is home (dashboard) load logTerm
if (window.location.pathname === '/' || window.location.hash === '#dashboard') {
    loadLogTerm();
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
        console.log(e.currentTarget.innerText);
        navigate(e.currentTarget.innerText);
        e.cancelBubble = true;
    });
});
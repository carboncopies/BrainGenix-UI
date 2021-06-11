axios.post('https://braingenix.org:2001/', {
        SysName: 'NES', 
        CallStack:'LFTM.SystemTelemetryManager.mAPI_GetAllNodeStats',
        KeywordArgs: {}
    }).then(function (response) {
        // handle success
        console.log(response);
        console.log(typeof(response.Content));
        for(var h in response.Content) {
            document.querySelector('#ram-usage .stat').innerText = response.Content[h].RAMUsage;
        }
    })
    .catch(function (error) {
        // handle error
        console.log(error);
    });
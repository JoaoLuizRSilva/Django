function renderiza_total(url, item){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        document.querySelector(`#${item}`).innerHTML = data.total
    })
}

function grafico_total_mensal(url, item, label){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        const ctx = document.querySelector(`#${item}`).getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: label,
                    data: data.data,
                    backgroundColor: '#3F51B5',
                    borderColor: '#fff',
                    borderWidth: 0.2
                }]
            }
        });
    })
}

function grafico_horizontal(url, item){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        const ctx = document.querySelector(`#${item}`).getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Modalidade',
                    data: data.data,
                    backgroundColor: '#012340',
                    borderColor: '#fff',
                    borderWidth: 0.2
                }]
            }
        });
    })
}

function grafico_pizza(url, item){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        const ctx = document.querySelector(`#${item}`).getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    label: data.labels,
                    data: data.data,
                    backgroundColor: ['#00A5DB', '#EA206D', '#764498'],
                    borderColor: '#fff',
                    borderWidth: 0.2
                }]
            }
        });
    })
}
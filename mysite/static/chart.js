
console.log('success');
$.ajax({
    method: "GET",
    url: 'get_data/',
    success: function(text){
        console.log('success');

        const label1 = text['NoComMon'];
        const label2 = text['ComMon'];

          const data = {
            labels: label1,
            datasets: [{
              label: 'NoComplated',
              backgroundColor: 'rgb(255, 99, 132)',
              borderColor: 'rgb(255, 99, 132)',
              borderWidth: 1,
              data: text['NoComTask'],
            }, {
              label: 'Complated',
              backgroundColor: 'blue',
              borderColor: 'blue',
              borderWidth: 1,
              data: text['ComTask'],
            },

            ]};
          let m = 1
            if(text['NoComTask'].length > 10){
                m = 2
            }else if(text['NoComTask'].length > 20){
                m = 4
            }else if(text['NoComTask'].length > 30){
                m = 5
            }
          const config = {
            type: 'bar',
            data: data,
            options: {
                   responsive: true,
                    legend: {
                      position: 'bottom'
                    },
                    scales: {

                       yAxes: [{
                            ticks: {
                                stepSize: m,
                                beginAtZero: true,
                                precision: 0
                            }

                        }],
                          y: {
                                beginAtZero: true
                              }
                            }
            }
          };

           const myChart = new Chart(
                document.getElementById('myChart'),
                config
          );
    },
    error: function(error_data){
        console.log("Error")
        console.log(error_data)
    }
})






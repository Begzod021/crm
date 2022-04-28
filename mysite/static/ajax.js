$.ajax({
    type: 'GET',
    url: '/employes-json/',
    success: function(response){
      console.log(response.data)
      const employesData = response.data
      employesData.map(item=>{
        const option = document.createElement('option')
        option.textContent = item.user
      })
    },
    error: function(error){
      console.log(error)
    },


  })  
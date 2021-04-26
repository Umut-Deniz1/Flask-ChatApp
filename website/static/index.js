  $(function() {
    $('#btn_sendmsg').bind('click', function() {
      var value = document.getElementById("msg").value;
      var element = document.getElementById('chat_text');
      element.scrollTop = element.scrollHeight;
      document.querySelector("#msg").value = "";
      
      $.getJSON('/run',
      {val:value},
          function(data) {
            console.log("test");   
      });
      
    });
  });

  $("#msg").on('keyup', function (e) {
    if (e.key === 'Enter' || e.keyCode === 13) {
       document.querySelector("#btn_sendmsg").click()
    }
  });


  window.addEventListener("load",function(){
    var update_loop = setInterval(update, 100)
    update()
  });

  function update(){
    fetch("/get_messages")
        .then(function (response){
          return response.json(); 
        }).then(function (text){

          var messages= "";
          for (value of text["messages"]){
            messages = messages + "<br >" + value;
          }
          document.getElementById("chat_text").innerHTML = messages;
        
        });   
      return false;
  }

  
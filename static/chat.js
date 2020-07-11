$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    window.onbeforeunload = function() {
		return "Leaving this page will end your ongoing game for everyone.";
	};

    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        console.log(data);
        if (data.type == 'alert'){
            alert(data.message)
        }
        if (data.type == 'unlock_question'){
            $('#question_container'+data.question_id).attr('hidden', false);
        }
        if (data.type == 'show_answer'){
			$('#player_answers_body').empty();
			// populate answers
            // Update Correct answer
            for(var i = 0; i < data.answers.length; i++){
                var player = data.answers[i].player;
                var answer = data.answers[i].answer;
                $('#player_answers_body').append($('<tr><td>'+player+'</td><td>'+answer+'</td></tr>'));
            }
			$('#AnswerModal').modal('show');
        }
        if (data.type == 'show_score'){
			$('#player_scores_body').empty();
			// populate
            for(var i = 0; i < data.scores.length; i++){
                var player = data.scores[i].player;
                var score = data.scores[i].score;
                $('#player_scores_body').append($('<tr><td>'+player+'</td><td>'+score+'</td></tr>'));
            }
			$('#ScoreModal').modal('show');
        }
        if (data.type == 'answer_response'){
           alert('Answer Submitted')
        }
    };

    $("#joingame").on("submit", function(event){
      if ($('#handle').val() && $('#handle').val().indexOf(' ') < 0){
          $('#handle').prop('readonly', true);
          var message = {
              handle: $('#handle').val(),
              type: 'join',
          }
          chatsock.send(JSON.stringify(message));
      }
      else{
        alert("Please enter a valid name without spaces");
      }
      return false;
    });

    $(".answer_question").on("submit", function(event) {
        if($('#handle').val()){
            var message = {
                handle: $('#handle').val(),
                type: 'answer',
                answer: $('#'+$(this).attr('question_id')+'_answer').val(),
                question: $(this).attr('question_id'),
            }
            chatsock.send(JSON.stringify(message));
        }
        else{
            alert("Please enter a handle without spaces.");
        }
        return false;
    });
	function heartbeat() {
		var message = {
			type: 'beat',
            handle: 'beat',
		}
		chatsock.send(JSON.stringify(message));
	}
	setInterval(heartbeat, 39999);

});

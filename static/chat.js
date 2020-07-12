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
            $('#question_container'+data.question_id).show();
			$([document.documentElement, document.body]).animate({
        		scrollTop: $('#q'+data.question_id+'_answer').offset().top
    		}, 1000);
            $('#q'+data.question_id+'_answer').pincodeInput().data('plugin_pincodeInput').focus();
        }
        if (data.type == 'show_answer'){
			$('#player_answers_body').empty();
			// populate answers
            // Update Correct answer
            $('#correct_answer').html('Correct Answer : '+data.correct_answer)
            for(var i = 0; i < data.answers.length; i++){
                var player = data.answers[i].player;
                var answer = data.answers[i].answer;
                var score = data.answers[i].score;
                $('#player_answers_body').append($('<tr><td>'+player+'</td><td>'+answer+'</td> <td>'+score+'</td></tr>'));
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

        // Admin type
        if (data.type == 'answer_admin'){
           $('#answers_list_'+data.question).append(data.by + '-' + data.ans + '<br>');
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
          $('#join').attr('disabled', 'disabled');
      }
      else{
        alert("Please enter a valid name without spaces");
      }
      return false;
    });

    $(".answer_question").on("submit", function(event) {
        if($('#handle').val()){
	    if($(this).attr('answer').length == $(this).attr('len')){
            var message = {
                handle: $('#handle').val(),
                type: 'answer',
                answer: $(this).attr('answer'),
                question: $(this).attr('question_id'),
            }
            chatsock.send(JSON.stringify(message));
        }
        else{
            alert("Please enter valid answer");
        }
        }
        else{
            alert("Please enter a handle without spaces.");
        }
        return false;
    });
    $(".unhide").click(function(){
            var message = {
                type: 'unlock_question',
                question: $(this).parent().attr('question_id'),
            }
            chatsock.send(JSON.stringify(message));
    });
    $(".lock").click(function(){
            var message = {
                type: 'lock_question',
                question: $(this).parent().attr('question_id'),
            }
            chatsock.send(JSON.stringify(message));
    });
    $(".show").click(function(){
            var message = {
                type: 'show_answers',
                question: $(this).parent().attr('question_id'),
            }
            chatsock.send(JSON.stringify(message));
    });
    $(".score_show").click(function(){
            var message = {
                type: 'show_scores',
            }
            chatsock.send(JSON.stringify(message));
    });
	function heartbeat() {
		var message = {
			type: 'beat',
            handle: 'beat',
		}
		chatsock.send(JSON.stringify(message));
	}
	setInterval(heartbeat, 39999);
    $(document) .ready(function(){
        $('.question_answer').each(function(){
		   var question_id = $(this).attr('question_id');
           $(this).pincodeInput({inputs:$(this).attr('len'), hidedigits:false, complete: function(value, e, error){
				$('#answer_question_'+question_id).attr('answer', value);
			}});
        });
        $('.hidden_question').each(function(){
            $(this).hide();
        });
    });


});

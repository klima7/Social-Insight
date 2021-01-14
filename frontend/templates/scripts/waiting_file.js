let packid = $('#packid').text()

function check() {
    $.ajax({
        dataType: "json",
        url: '/api/files/progress',
        cache: false,
        success: function(data) {
			console.log(data);
			if(data.progress != null) {
				$('#progress').text(data.progress)
				if(data.ready) {
					window.location.href = '/files/download';
					$('#message').text('{{ _('Here you are!') }} ')
					setTimeout(() => window.close(), 2000);
				}
				else setTimeout(check, 500);
            }
        },
        error: function() {
            alert("Error occured on progress check");
        }
    });
}

setTimeout(check, 2000);

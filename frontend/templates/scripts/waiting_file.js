let file_id = {{ file_id }};

function check() {
    $.ajax({
        dataType: "json",
        url: `/api/files/${file_id}/progress`,
        cache: false,
        success: function(data) {
			if(data.progress != null) {
				$('#progress').text(data.progress)
				if(data.ready) {
					window.location.href = `/files/${file_id}/download`;
					$('#message').text('{{ _('Here you are!') }} ')
					setTimeout(() => window.close(), 2000);
				}
				else setTimeout(check, 20);
            }
        },
        error: function() {
            alert("Error occured on progress check");
        }
    });
}

check();

let file_id = {{ file_id }};
let visible_progress = 0;
let real_progress = 0;
let ready = false;

function check() {
    $.ajax({
        dataType: "json",
        url: `/api/files/${file_id}/progress`,
        cache: false,
        success: function(data) {
			if(data.progress != null) {
				real_progress = data.progress;
				ready = data.ready;
				if(!ready)
					setTimeout(check, 20);
            }
        },
        error: function() {
            alert("Error occured on progress check");
        }
    });
}

let intervalId = setInterval(function() {
	if(visible_progress < real_progress) {
		visible_progress += 1;
		$('#progress').text(visible_progress)
	}

	if(visible_progress==100 && ready) {
		window.location.href = `/files/${file_id}/download`;
		$('#message').text('{{ _('Here you are!') }} ')
		setTimeout(() => window.close(), 2000);
		clearInterval(intervalId);
	}
}, 25);

check();

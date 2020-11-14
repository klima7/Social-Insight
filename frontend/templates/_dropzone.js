const API_PREFIX = 'api/';

Dropzone.options.uploadZone = {
    maxFilesize: 10000000,
    timeout: 1000000000000,
    maxFiles: 1,
    createImageThumbnails: false,
    acceptedFiles: ".zip",
    clickable: '#uploadLogo',

    dictFileTooBig: 'This file is too big',
    dictInvalidFileType: 'Only zip files are acceptible',
    dictResponseError: 'Server response is invalid',

    init: function() {
    	dz = this;

  		this.on("uploadprogress", function(file, progress) {
			if(progress == 100) check()
  		});

    	this.on("addedfile", function(newfile) {
			for(let file of dz.files) {
				if(file != newfile)
					dz.removeFile(file);
			}
     	});
    }
}

function check() {
    $.ajax({
        dataType: "json",
        url: API_PREFIX + "packs/anonymous/ready",
        cache: false,
        success: function(data) {
            console.log(data);
            if(data.done==true) {
                fetchGraphs()
            }
            else {
                setTimeout(check, 1000);
            }
        },
        error: function() {
            alert("Error occured on ready check");
        }
    });
}

function fetchGraphs() {
    $.ajax({
        dataType: "html",
        url: API_PREFIX + "packs/anonymous/graphs",
        cache: false,
        success: function(data) {
            $("#graphs").html(data);
        },
        error: function() {
            alert("Error occured on graphs fetch");
        }
    });
    Dropzone.forElement('#uploadZone').removeAllFiles(true)
}

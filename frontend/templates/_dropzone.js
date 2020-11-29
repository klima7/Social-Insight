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

//  		this.on("uploadprogress", function(file, progress) {
//			if(progress == 100) {
//				window.location.href = '/packs/waiting';
//			}
//  		});

  		this.on("success", function(file, responseText) {
			console.log(responseText.id);
			window.location.href = `/packs/waiting/${responseText.id}`;
        });

    	this.on("addedfile", function(newfile) {
			for(let file of dz.files) {
				if(file != newfile)
					dz.removeFile(file);
			}
     	});
    }
}

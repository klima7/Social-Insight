Dropzone.options.uploadZone = {
    maxFilesize: 10000000,
    timeout: 1000000000000,
    maxFiles: 1,
    createImageThumbnails: false,
    acceptedFiles: ".zip",
    clickable: '#uploadLogo',

    dictFileTooBig: "{{ _('This file is too big') }}",
    dictInvalidFileType: "{{ _('Only zip files are acceptible') }}",
    dictResponseError: "{{ _('Server response is invalid') }}",

    init: function() {
    	dz = this;

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

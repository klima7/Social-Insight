const API_PREFIX = 'api/'

Dropzone.options.myDropzone = {
    maxFilesize: 10000000,
    timeout: 1000000000000,
    maxFiles: 1,
    dictFileTooBig: 'Plik jest za duży',
    dictInvalidFileType: 'Akceptowane są jedynie pliki json',
    dictMaxFilesExceeded: 'Możliwe jest dołączenie tylko jednego pliku',
    init: function() {
      this.on("uploadprogress", function(file, progress) {
        if(progress == 100) check()
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
                console.log("Done");
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
            console.log(data);
            $("#graphs").html(data);
        },
        error: function() {
            alert("Error occured on graphs fetch");
        }
    });
    Dropzone.forElement('#myDropzone').removeAllFiles(true)
}

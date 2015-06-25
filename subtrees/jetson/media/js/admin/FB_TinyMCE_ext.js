var FileBrowserDialogue = {
    init: function() {
        // remove tinymce stylesheet.
        var allLinks = document.getElementsByTagName("link");
        allLinks[allLinks.length-1].parentNode.removeChild(allLinks[allLinks.length-1]);
    },
    fileAndDescriptionSubmit: function(file) {
        var URL = file.file_path;
        var win = tinyMCEPopup.getWindowArg("window");
        // insert information now
        win.document.getElementById(tinyMCEPopup.getWindowArg("input")).value = URL;
        
        // change width/height & show preview
        if (win.ImageDialog){
            win.document.getElementById("alt").value = file.title;
            win.document.getElementById("title").value = file.title;
            win.document.getElementById("description").value = file.description;
            win.document.getElementById("author").value = file.author;
            if (win.ImageDialog.getImageData)
                win.ImageDialog.getImageData();
            if (win.ImageDialog.showPreviewImage)
                win.ImageDialog.showPreviewImage(URL);
        }
        
        // close popup window
        tinyMCEPopup.close();
    }
}

tinyMCEPopup.onInit.add(FileBrowserDialogue.init, FileBrowserDialogue);


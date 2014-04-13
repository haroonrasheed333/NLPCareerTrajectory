$(document).ready(function () {

    added_files = []

    $('#file-upload').fileupload({
        dataType: 'json',
        singleFileUploads: true,
        forceIframeTransport: true,
        url: '/analyze',
        add: function (e, data) {
            added_files.push(data);
            console.log(added_files);
            $('#uploadbutton').unbind('click');
            $('#uploadbutton').on('click', function(e) {
                e.preventDefault();
                data.formData = $('#file-upload').serializeArray();
                var original_data = data;
                var new_data = {files: [], originalFiles: [], paramName: []};
                jQuery.each(added_files, function(index, file) {
                    new_data['files'] = jQuery.merge(new_data['files'], file.files);
                    new_data['originalFiles'] = jQuery.merge(new_data['originalFiles'], file.originalFiles);
                    new_data['paramName'] = jQuery.merge(new_data['paramName'], file.paramName);
                    });
                new_data = jQuery.extend({}, original_data, new_data);
                console.log(new_data);
                new_data.submit();
            });
        },
        submit: function (e, data) {
            console.log(data);
        },
        done: function (e, data) {
            console.log(data);
        },
        send: function (e, data) {
            console.log(data);
        },
        success: function(data1){            

            $('#analyze').click(function(){

            console.log("yay");

            })

        }


})


})
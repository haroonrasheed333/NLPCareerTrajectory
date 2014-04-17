$(document).ready(function () {

    added_files = []

    $('#fileupload').fileupload({
        dataType: 'json',
        singleFileUploads: true,
        forceIframeTransport: true,
        url: '/analyze',
        add: function (e, data) {
            added_files = []
            added_files.push(data);
            console.log(added_files);
            $('#upload-button').unbind('click');
            $('#upload-button').on('click', function(e) {
                e.preventDefault();
                data.formData = $('#fileupload').serializeArray();
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
        success: function(data){
                console.log("logging data");
                console.log(data);
                var employer =[];
                var title = [];
                var predicted=[];
                data.employer.forEach(function(aa){
                    employer.push(aa)
                });
                console.log(employer);
                data.title.forEach(function(aa){
                    title.push(aa)
                });

                data.predicted.forEach(function(aa){
                    predicted.push(aa)
                });
                var link1="http://www.simplyhired.com/k-";
                var link3="-jobs.html";
                var table = document.getElementById("predictions");
                console.log(table);
                var i =0;
                console.log(predicted.length);
                while(i<predicted.length){
                    console.log('here');
                    var row = table.insertRow(i+1);
                    var cell = row.insertCell(0);
                    var predictnew = predicted[i].replace(" ","-" );
                    var newText  = document.createTextNode(predicted[i])
                    cell.appendChild(newText);
                    console.log(cell);
                    cell.title = predicted[i];
                    cell.href = link1.concat(predicted[i].concat(link3))
                    
                    // cell.innerHTML = link1.concat(predicted[i][0].concat(link3));

                   
                    i++;
                    // cell="hi:"predicted[rows];
                }

                    if (table != null) {
                        for (var i = 0; i < table.rows.length; i++) {
                            for (var j = 0; j < table.rows[i].cells.length; j++)
                                table.rows[i].cells[j].onclick = function () { onclick(this); };
                        }
                    }
             
                    function onclick(cel) {
                        window.open(cel.href);
                    }
                $('#predictions tr td').click(function(){
                    console.log($(this));
                })
               
                // cell.onclick=function(){
                //         window.open(link1.concat(predicted[i][0].concat(link3)),'_blank');
                //         console.log(link1.concat(predicted[i][0].concat(link3)));
                //     }



                var table1 = document.getElementById("network");
                console.log(table1);
                var i =0;
                console.log(employer.length+title.length);
                while(i<(employer.length+title.length)){
                    if (i<employer.length){

                    
                    console.log('here');
                    var row = table1.insertRow(i+1);
                    var cell = row.insertCell(0);
                    var newText  = document.createTextNode(employer[i])
                    cell.appendChild(newText);
                    console.log(cell);
                    i++;
                }
                else
                {
                   console.log('here');
                    var row = table1.insertRow(i+1);
                    var cell = row.insertCell(0);
                    var newText  = document.createTextNode(title[i-(employer.length)])
                    cell.appendChild(newText);
                    console.log(cell);
                    i++; 
                }
                    // cell="hi:"predicted[rows];
                }
        
}




})


})
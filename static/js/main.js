$(document).ready(function () {

    added_files = []

    $('#fileupload').fileupload({
        dataType: 'json',
        singleFileUploads: true,
        forceIframeTransport: true,
        url: '/analyze',
        add: function (e, data) {;
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

        success: function(data) {

            console.log("logging data");
            console.log(data);
            var employer =[];
            var title = [];
            var predicted=[];
            var skills_map = [];
            data.employer.forEach(function(aa){
                employer.push(aa);
            });
            console.log(employer);
            data.title.forEach(function(aa){
                title.push(aa);
            });

            data.predicted.forEach(function(aa){
                predicted.push(aa);
            });

            data.skills_map.forEach(function(aa){
                skills_map.push(aa);
            });

            console.log("hr");
            console.log(skills_map);

            var link1="http://www.simplyhired.com/k-";
            var link3="-jobs.html";
            // window.location.href = "/";
            $("#predictions").remove();
            console.log()
            // $("#predictions-div").append($('<h4>Your top 5 Job predictions</h4>'));
            $("#predictions-div").append($('<table id="predictions"></table>'));
            var table = document.getElementById("predictions");
            console.log(table);
            var i =0;
            console.log(predicted.length);

            var thead = document.createElement('thead');
            table.appendChild(thead);
            thead.appendChild(document.createElement("th")).appendChild(document.createTextNode("Your top 5 Job predictions"));

            while(i<predicted.length) {
                console.log('here');
                var row = table.insertRow(i);
                var cell = row.insertCell(0);
                var predictnew = predicted[i].replace(" ","-" );
                var newText  = document.createTextNode(predicted[i]);
                cell.appendChild(newText);
                console.log(cell);
                cell.title = predicted[i];
                cell.href = link1.concat(predicted[i].concat(link3));
                i++;
            }
            $("#predictions-div").append(table)

            if (table != null) {
                for (var i = 0; i < table.rows.length; i++) {
                    for (var j = 0; j < table.rows[i].cells.length; j++){
                        table.rows[i].cells[j].onMouseover = function () { onhover(this); };
                        table.rows[i].cells[j].onclick = function () { onclick(this); };
                    }
                }
            }
            function onclick(cel) {
                window.open(cel.href);
            }
            function onhover(cel){
                console.log("eeeeee");
                this.bgColor='#33CCFF';
            }
            $("#skills-div").empty();
            // $("#skills-table").remove();
            // $("div.skills-div").text()="";



            var sel1 = $('<select id="skill-map">');
            sel1.append($("<option>").attr('value', '0').text("Select a Title"));
            for (var i = 0; i < predicted.length; i++) {
                sel1.append($("<option>").attr('value', predicted[i]).text(predicted[i]));
            }
            $("#skills-div").append($('<h4>Top Skills</h4>'));
            $("#skills-div").append(sel1);

            // Dynamically create input options.
            $( "#skill-map" ).change(function() {
                $( "#skills-table" ).remove();
                var title = $(this).val();
                if (title != '0') {
                    var skill_table = $('<table id="skills-table"></table>');
                    skill_table.append($('<tr><th>Skill</th><th>Percent</th></tr>'))
                    for (var j = 0; j < skills_map.length; j++) {
                        var skills = [];
                        var percents = [];
                        if (title in skills_map[j]) {
                            skills = skills_map[j][title]['skills'];
                            percents = skills_map[j][title]['percent'];
                            for (var k = 0; k < 10; k++) {
                                skill_table.append($('<tr><td>' + skills[k] + '</td><td>' + percents[k] + '</td></tr>'));
                            }
                        }
                    }
                    $("#skills-div").append(skill_table);
                }
            });

            $( "#network" ).append($('<a href="http://127.0.0.1:5000/network"><h5>What are my alumni doing</h5></a><h5><a href="http://127.0.0.1:5000/network"></a></h5>'));

//            // $("#predictions-div").append($('<h4>Your top 5 Job predictions</h4>'));
//            $("#network-div").append($('<table id="network"></table>'));
//
//            var table1 = document.getElementById("network");
//            console.log(table1);
//            var i =0;
//            console.log(employer.length+title.length);
//            var thead1 = document.createElement('thead');
//
//            table1.appendChild(thead1);
//            thead1.appendChild(document.createElement("th")).appendChild(document.createTextNode("Top Employers and Job titles for your specialization"));
//
//            while(i<(employer.length+title.length)){
//                if (i<employer.length){
//
//                console.log('here');
//                var row = table1.insertRow(i);
//                var cell = row.insertCell(0);
//                var newText  = document.createTextNode(employer[i])
//                cell.appendChild(newText);
//                console.log(cell);
//                i++;
//            }
//            else
//            {
//               console.log('here');
//                var row = table1.insertRow(i);
//                var cell = row.insertCell(0);
//                var newText  = document.createTextNode(title[i-(employer.length)])
//                cell.appendChild(newText);
//                console.log(cell);
//                i++;
//            }
//        }
    }
});
});
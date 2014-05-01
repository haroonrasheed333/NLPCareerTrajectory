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
                new_data.submit();
            });
        },
        submit: function (e, data) {
        },
        done: function (e, data) {

        },
        send: function (e, data) {
        },

        success: function(data) {

            var employer =[];
            var title = [];
            var predicted=[];
            var skills_map = [];
            var all_titles = [];
            data.employer.forEach(function(aa){
                employer.push(aa);
            });
            data.title.forEach(function(aa){
                title.push(aa);
            });

            data.predicted.forEach(function(aa){
                predicted.push(aa);
            });

            data.skills_map.forEach(function(aa){
                skills_map.push(aa);
            });

            data.titles.forEach(function(aa){
                all_titles.push(aa);
            });


            var link1="http://www.simplyhired.com/k-";
            var link3="-jobs.html";
            var i = 0;

            $("#predictions-div").empty();

            $("#predictions-div").append($('<h3 class="center-text">Your Top 5 Job Predictions</h3>'))

            $("#predicted-titles-list" ).remove();
            var predicted_titles_list = $('<ul id="predicted-titles-list"></ul>');

            for (var i = 0; i < predicted.length; i++) {
                var li;

                if (i % 2 == 0) {
                    li = $('<li class="even-row"></li>');
                } else {
                    li = $('<li></li>');
                }

                var href = link1.concat(predicted[i].concat(link3));
                cand_skill_list = data.candidate_skills[predicted[i]];
                li.append($('<div title="' + predicted[i] + '"><a target="_blank" href="' + href + '">' + predicted[i] + '</a></div>'));

                var skill_div = $('<div class="skills-list-div"></div>');
                var skill_ul = $('<ul class="skills-list"></ul>');

                skill_div.append(skill_ul);

                for (var k = 0; k < cand_skill_list.length; k++) {
                    skill_ul.append($('<li>· ' + cand_skill_list[k] + '</li>'));
                }

                li.append(skill_div);

                predicted_titles_list.append(li);
            }

            $("#predictions-div").append(predicted_titles_list);

            $("#skills-div").empty();

            var sel1 = $('<select id="skill-map">');
            sel1.append($("<option>").attr('value', '0').text("Select a Title"));
            for (var i = 0; i < all_titles.length; i++) {
                sel1.append($("<option>").attr('value', all_titles[i]).text(all_titles[i]));
            }
            $("#skills-div").append($('<h3>Top Skills</h3>'));
            $("#skills-div").append(sel1);

            $('#skill-map').val(predicted[0]);
            $( "#skills-table" ).remove();
            var title = predicted[0]
            if (title != '0') {
                var skill_table = $('<table id="skills-table"></table>');
                for (var j = 0; j < skills_map.length; j++) {
                    var skills = [];
                    var percents = [];
                    if (title in skills_map[j]) {
                        skills = skills_map[j][title]['skills'];
                        percents = skills_map[j][title]['percent'];
                        for (var k = 0; k < 20; k++) {
                            skill_table.append($('<tr><td>' + skills[k] + '</td><td>' + percents[k] + '</td></tr>'));
                        }
                    }
                }
                $("#skills-div").append(skill_table);
            }

            // Dynamically create input options.
            $( "#skill-map" ).change(function() {
                $( "#skills-table" ).remove();
                var title = $(this).val();
                if (title != '0') {
                    var skill_table = $('<table id="skills-table"></table>');
                    for (var j = 0; j < skills_map.length; j++) {
                        var skills = [];
                        var percents = [];
                        if (title in skills_map[j]) {
                            skills = skills_map[j][title]['skills'];
                            percents = skills_map[j][title]['percent'];
                            for (var k = 0; k < 20; k++) {
                                skill_table.append($('<tr><td>' + skills[k] + '</td><td>' + percents[k] + '</td></tr>'));
                            }
                        }
                    }
                    $("#skills-div").append(skill_table);
                }
            });

            $("#network").empty();
            $("#network").append($('<a href="http://127.0.0.1:5000/network"><h5>What are my alumni doing</h5></a><h5><a href="http://127.0.0.1:5000/network"></a></h5>'));

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
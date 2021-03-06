$(document).ready(function () {

    $( document ).tooltip();

    $('.collapse-class').live('click', function () {
        var id = $(this).attr('id');
        var no = id.substring(9);
        $('#more-' + no).slideToggle(255);
    });

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
            $('#spinner-id').css('display', 'inline-block');
        },
        done: function (e, data) {

        },
        send: function (e, data) {
        },

        success: function(data) {

            response_data = data;
            sessionStorage.setItem('response', JSON.stringify(data));
            var resp_temp = sessionStorage.getItem('response');
            sessionStorage.setItem('university', $.parseJSON(resp_temp).university);
            sessionStorage.setItem('tree_json', $.parseJSON(resp_temp).tree_json);
            populateData(data);
            // console.log(location);
            // location.href = location.origin + '/results_home';
        }
    });

    $(window).load(function() {
        url_pathname = location.pathname;
        // if (url_pathname == "/results_home") {
        //     $.ajax({
        //        datatype: 'json',
        //        url: '/results',
        //        success: function(data)
        //        {
        //            populateData(data);
        //        }
        //      });
        // }

        if (url_pathname == "/") {
            var temp1 = sessionStorage.getItem('response');
            data =  $.parseJSON(temp1);
            populateData(data);
        }
    });

    $('#logo-img-home').click(function() {
        sessionStorage.removeItem('response');
        sessionStorage.removeItem('university');
        sessionStorage.removeItem('tree_json');
        location.href = location.origin + '/';
    });

    function populateData(data) {
        var predicted=[];
        var skills_map = [];
        var all_titles = [];
        var scores = [];

        // data = $.parseJSON(data);
        // console.log(data);

        data.final_prediction_list.forEach(function(aa){
            predicted.push(aa);
        });
        data.final_score_sorted.forEach(function(aa){
            scores.push(aa);
        });
        data.skills_map.forEach(function(aa){
            skills_map.push(aa);
        });
        data.titles.forEach(function(aa){
            all_titles.push(aa);
        });

        // console.log(data.title_data);

        var link1 = "http://www.simplyhired.com/k-";
        var link3 = "-l-san-francisco-ca-jobs.html";
        var i = 0;

        $("#predictions-div").empty();
        $('#spinner-id').css('display', 'none');
        $("#predictions-div").append($('<div class="column-90 column block-title"><h3>Your Top Matches</h3></div><div class="column-10 column block-title"><h3><i class="fa fa-info-circle" title="Your top job predictions are determined based on various factors like your skills, education, degree level etc. We compare you against others similar to you to help you decide what your prospective next step could be"></i></h3></div>'))
        $("#predicted-titles-list" ).remove();
        var predicted_titles_list = $('<ul id="predicted-titles-list"></ul>');

        for (var i = 0; i < 5; i++) {
            var li;
            if (i % 2 == 0) {
                li = $('<li class="even-row collapse-class" id="collapse-' + i + '"></li>');
            } else {
                li = $('<li class="collapse-class" id="collapse-' + i + '"></li>');
            }
            var href = link1.concat(predicted[i].concat(link3));
            cand_skill_list = data.candidate_skills[predicted[i]];

            li.append($('<div>' + predicted[i] + '<div id="score-div"><span class="score" title="Your Match Score">' + scores[i] + '</span><div class="bar-div" title=""><span class="bar" id="bar1-' + i + '"></span><span class="bar" id="bar2-' + i + '"></span><span class="bar" id="bar3-' + i + '"></span></div></div></div>'));

            var skill_div = $('<div class="skills-list-div"></div>');
            var skill_ul = $('<ul class="skills-list"></ul>');
            skill_ul.append($('<li><strong>Your Matching Skills:</strong></li>'));

            skill_div.append(skill_ul);

            for (var k = 0; k < cand_skill_list.length; k++) {
                skill_ul.append($('<li>· ' + cand_skill_list[k] + '</li>'));
            }
            if (k !=0){
                li.append(skill_div);
            }


            var more_info = $('<div class="more-info-div" id="more-' + i + '"></div>');
            more_info.append($('<div><span><strong>Salary (US National Average): </strong>' + data.title_data[predicted[i]]["salary"] + '</div></span>'));
            more_info.append($('<div><span><strong>Expected Education Level: </strong>' + data.title_data[predicted[i]]["education"] + '</div></span>'));
            // more_info.append($('<div><span><strong>Average Experience: </strong>5 Years</div></span>'));
            more_info.append($('<div><span><strong>Projected Jobs (2012 - 2022): </strong>' + data.title_data[predicted[i]]["trends"]["Projected job openings (2012-2022)"] + '</div></span>'));
            more_info.append($('<div><span><strong>Projected Growth (2012 - 2022): </strong>' + data.title_data[predicted[i]]["trends"]["Projected growth (2012-2022)"] + '</div></span>'));
            var rel_job = '';
            for (var a = 0; a < data.title_data[predicted[i]]["related_titles"].length; a++) {
                if (a != data.title_data[predicted[i]]["related_titles"].length - 1){
                rel_job = rel_job + data.title_data[predicted[i]]["related_titles"][a] + ', '
                }
                else{
                   rel_job = rel_job + data.title_data[predicted[i]]["related_titles"][a]
                }
            }
            if (rel_job) {
                more_info.append($('<div><span><strong>Related Job Titles: </strong>' + rel_job + '</div></span>'));
            }
            more_info.append($('<div><span><a target="_blank" href="' + href + '">Search ' + predicted[i] + ' Jobs</a></div></span>'));

            if (k !=0){
            li.append(more_info);
            predicted_titles_list.append(li);
            }
        }

        $("#predictions-div").append(predicted_titles_list);

        for (var i = 0; i < scores.length; i++) {
            if (scores[i] < 40) {
                $('#bar3-' + i).css("background", "#78ECE8");
                $('#bar2-' + i).css("background", "#78ECE8");
            } else if (scores[i] < 70) {
                $('#bar3-' + i).css("background", "#78ECE8");
            }
        }
        $("#skills-div").empty();

        var sel1 = $('<select id="skill-map">');
        sel1.append($("<option>").attr('value', '0').text("Select a Title"));
        for (var i = 0; i < all_titles.length; i++) {
            sel1.append($("<option>").attr('value', all_titles[i]).text(all_titles[i]));
        }
        $("#skills-div").append($('<div class="column-90 column block-title"><h3>Top Skills For Jobs</h3></div><div class="column-10 column block-title"><h3><i class="fa fa-info-circle" title="Select a Job and find out what skills are most important to land at the selected job"></i></h3></div>'));
        $("#skills-div").append(sel1);

        $('#skill-map').val(predicted[0]);
        $( "#title-skills-list" ).remove();
        var title = predicted[0]

        if (title != 0) {
            var title_skills_ul = $('<ul id="title-skills-list"></ul>');
            for (var j = 0; j < skills_map.length; j++) {
                var skills = [];
                var percents = [];
                if (title in skills_map[j]) {
                    skills = skills_map[j][title]['skills'];
                    percents = skills_map[j][title]['percent'];
                    var num_skills = 15;
                    if (num_skills > skills.length) {
                        num_skills = skills.length;
                    }
                    for (var k = 0; k < num_skills; k++) {
                        title_skills_ul.append($('<li><div class="skill-name"><h5>' + skills[k] + '</h5></div><div class="skill-percent"><h5>' + percents[k] + '</h5></div></li>'));
                    }
                }
            }
            $("#skills-div").append(title_skills_ul);
            $("footer").css("display", "block");
        }
        // Dynamically create input options.
        $( "#skill-map" ).change(function() {
            $( "#title-skills-list").remove();
            var title = $(this).val();
            if (title != '0') {
                var title_skills_ul = $('<ul id="title-skills-list"></ul>');
                for (var j = 0; j < skills_map.length; j++) {
                    var skills = [];
                    var percents = [];
                    if (title in skills_map[j]) {
                        skills = skills_map[j][title]['skills'];
                        percents = skills_map[j][title]['percent'];
                        var num_skills = 15;
                        if (num_skills > skills.length) {
                            num_skills = skills.length;
                        }
                        for (var k = 0; k < num_skills; k++) {
                            title_skills_ul.append($('<li><div class="skill-name"><h5>' + skills[k] + '</h5></div><div class="skill-percent"><h5>' + percents[k] + '</h5></div></li>'));
                        }
                    }
                }
                $("#skills-div").append(title_skills_ul);
            }
        });

        $(".more-info-div").hide();

        $('#skill-search').empty();
        $('#skill-search').append($('<div class="column-90 column block-title"><h3>Skill Search</h3></div><div class="column-10 column block-title"><h3><i class="fa fa-info-circle" title="Have a niche skill? Search for your skills to explore what jobs require your special skill"></i></h3></div>'));
        var skill_input_div = $('<div class="column-100 column" id="skill-search-input"><input type="text" name="skill" id="skill-ajax" style="position: relative; z-index: 2;"/><button id="skill-submit-button" class="btn btn-primary pull-right" type="submit"><i class="fa fa-search"></i></button></div><input type = "hidden" type="text" name="skill" id="skill-ajax-x" disabled="disabled" style="color: #CCC; absolute: relative; background: transparent; z-index: 1;"/></div>');
        $('#skill-search').append(skill_input_div);


        // Initialize ajax autocomplete:
        $('#skill-ajax').autocomplete({
            // serviceUrl: '/autosuggest/service/url',
            lookup: skillsArray,
            lookupFilter: function(suggestion, originalQuery, queryLowerCase) {
                var re = new RegExp('\\b' + $.Autocomplete.utils.escapeRegExChars(queryLowerCase), 'gi');
                return re.test(suggestion.value);
            },
            onSelect: function(suggestion) {
                document.getElementById("skill-ajax").value = suggestion.value;
            },
            onHint: function (hint) {
                $('#skill-ajax-x').val(hint);
            },
            onInvalidateSelection: function() {
            }
        });

        $("#skill-submit-button").on('click',function() {
            $("#skill-search-input").css("margin-bottom", "10px");
            $("#skill-titles-list").remove();
            var skill_input = document.getElementById("skill-ajax").value;
            $.ajax({
               datatype: 'json',
               url: '/skill_submit',
               type: 'POST',
               data : {"skill": JSON.stringify(skill_input)},
               success: function(data)
               {
                    if (data) {
                        data = $.parseJSON(data);
                        var skill_titles_ul = $('<ul id="skill-titles-list"></ul>');
                        for (var j = 0; j < data.length; j++) {
                            skill_titles_ul.append($('<li><h5>' + data[j] + '</h5></li>'));
                        }
                        $("#skill-search").append(skill_titles_ul);
                    }
               }
            });
        });

        $('.bar-div').tooltip({ content: '<img src="../static/images/bar.png" />' });

    }
});
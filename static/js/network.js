var university = document.getElementById("university").value;
// console.log(document.getElementById("university").value);

var skillsEmployer, univNumberMap;

$(document).ready(function () {


// Trying to create data for network graph from JS -- Not Usin
//function create_data(univ, major, skills_employer, univ_major_map){
//    univ = univ.toString().toLowerCase();
//    major = major.toString().toLowerCase();
//    var result = {};
//    result["links"] = [];
//    if (univ in univ_major_map){
//        var indices = [];
//        if (major == null){
//            for (key in univ_major_map[univ]){
//                indices.push(univ_major_map[univ][key]);
//            }
//        }
//        else{
//            if (major in univ_major_map[univ]){
//                indices.push(univ_major_map[univ][major]);
//            }
//        }
//    }
//    for (index in indices){
//        if (index.toString() in skills_employer){
//            for (d in skills_employer[str(index)]["links"]){
//                result["links"].append(d);
//            }
//        }
//    }
//}




$("#inputs").empty;

if (university.length > 2) {
  var h3 = $('<h3>Displaying alumni network for all majors from your university. Key in your major to filter the network</h3><br>');
  var form = $('<form id="input-form"></form>');
  var major_div = $('<div class="column-33 column"><input type="text" name="major" id="major-ajax" style="position: relative; z-index: 2; background: transparent;"/></div>');
  var submit_button = $('<div class="column-25 column"><input id="network-submit-button" class="btn btn-primary pull-right" type="submit" value="Re-create network" /></div>');

  $("#inputs").append(h3);
  form.append(major_div);
  $("#inputs").append(form);
  $("#inputs").append(submit_button);
  create_network();

} else {

  var h3 = $('<h3>Key in your university and major to generate your alumni network</h3><br>');
  var form = $('<form id="input-form"></form>');
  var univ_div = $('<div class="column-33 column"><input type="text" name="university" id="university-ajax" style="position: relative; z-index: 2; background: transparent;"/></div>');
  var major_div = $('<div class="column-33 column"><input type="text" name="major" id="major-ajax" style="position: relative; z-index: 2; background: transparent;"/></div>');
  var submit_button = $('<div class="column-25 column"><input id="network-submit-button" class="btn btn-primary pull-right" type="submit" value="Create network" /></div>');

  $("#inputs").append(h3);
  form.append(univ_div);
  form.append(major_div);
  $("#inputs").append(form);
  $("#inputs").append(submit_button);

    // $("#inputs").append('<h3> Key in your university and major to generate your alumni network</h3></br>');
    // $("#inputs").append('<form id = "input-form"><div class="column-33 column"><input type="text" name="university" id="university-ajax" style="position: relative; z-index: 2; background: transparent;"/><input type = "hidden" type="text" name="university" id="university-ajax-x" disabled="disabled" style="color: #CCC; absolute: relative; background: transparent; z-index: 1;"/></div>')
    // $("#inputs").append('<div class="column-33 column"><input type="text" name="major" id="major-ajax" style="position: relative; z-index: 2; background: transparent;"/><input type = "hidden" type="text" name="country" id="major-ajax-x" disabled="disabled" style="color: #CCC; position: absolute; background: transparent; z-index: 1;"/></div>')
    // $("#inputs").append('<div class="column-25 column"><input id="network-submit-button" class="btn btn-primary pull-right" type="subimt" value="Create network" style="position: absolute;" /></div></form>');
//    create_network();

}



 $("#network-submit-button").on('click',function(){

    if (university.length > 2){
        var major_input = document.getElementById("major-ajax").value;

        $.ajax({
           datatype: 'json',
           url: '/submit',
           type: 'POST',
           data : {"major": JSON.stringify(document.getElementById("major-ajax").value)},
           success: function(data)
           {
               // console.log(data);
               $("#network-graph").remove();
               $("body").append($('<div id ="network-graph" class = column-100></div>'));
               create_network();
           }
         });

    } else {

        var major_input = document.getElementById("major-ajax").value;
        var university_input = document.getElementById("university-ajax").value;

        $.ajax({
           datatype: 'json',
           url: '/submit',
           type: 'POST',
           data : {"major": JSON.stringify(major_input), "university": JSON.stringify(university_input)},
           success: function(data)
           {
               // console.log(data);
               $("#network-graph").remove();
               $("body").append($('<div id ="network-graph" class="column-100"></div>'));
               create_network();
           }
         });

    }


 })



// Initialize ajax autocomplete:
$('#major-ajax').autocomplete({
    // serviceUrl: '/autosuggest/service/url',
    lookup: majorsArray,
    lookupFilter: function(suggestion, originalQuery, queryLowerCase) {
        var re = new RegExp('\\b' + $.Autocomplete.utils.escapeRegExChars(queryLowerCase), 'gi');
        return re.test(suggestion.value);
    },
    onSelect: function(suggestion) {

        document.getElementById("major-ajax").value = suggestion.value;
        $('#selction-ajax').html('You selected: ' + suggestion.value + ', ' + suggestion.data);
    },
    onHint: function (hint) {
        $('#autocomplete-ajax-x').val(hint);
    },
    onInvalidateSelection: function() {
        $('#selction-ajax').html('You selected: none');
    }
});

// Initialize ajax autocomplete:
$('#university-ajax').autocomplete({
    // serviceUrl: '/autosuggest/service/url',
    lookup: univsArray,
    lookupFilter: function(suggestion, originalQuery, queryLowerCase) {
        var re = new RegExp('\\b' + $.Autocomplete.utils.escapeRegExChars(queryLowerCase), 'gi');
        return re.test(suggestion.value);
    },
    onSelect: function(suggestion) {
        document.getElementById("university-ajax").value = suggestion.value;
        $('#selction-ajax').html('You selected: ' + suggestion.value + ', ' + suggestion.data);
    },
    onHint: function (hint) {
        $('#autocomplete-ajax-x').val(hint);
    },
    onInvalidateSelection: function() {
        $('#selction-ajax').html('You selected: none');
    }
});

function create_network(){
d3.json("../static/miserables.json", function(error, json) {

var links = json.links;
// console.log(links);

var nodes = {};

// Compute the distinct nodes from the links.
links.forEach(function(link) {
  link.source = nodes[link.source] || (nodes[link.source] = {name: link.source, size: 15});
  link.target = nodes[link.target] || (nodes[link.target] = {name: link.target, size: 6});
});


var width = 1200,
    height = 800;

var force = d3.layout.force()
    .nodes(d3.values(nodes))
    .links(links)
    .size([width, height])
    .gravity(.5)
    .linkDistance(150)
    .charge(-300)
    .on("tick", tick)
    .start();

var linkedByIndex = {};
json.links.forEach(function(d) {
    linkedByIndex[d.source.index + "," + d.target.index] = 1;
});

function isConnected(a, b) {
    return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
}
var svg = d3.select("#network-graph").append("svg")
    .attr("width", width)
    .attr("height", height);

// Per-type markers, as they don't inherit styles.
svg.append("defs").selectAll("marker")
    .data(["suit", "licensing", "resolved"])
  .enter().append("marker")
    .attr("id", function(d) { return d; })
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 15)
    .attr("refY", -1.5)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
  .append("path")
    .attr("d", "M0,-5L10,0L0,5");

var path = svg.append("g").selectAll("path")
    .data(force.links())
  .enter().append("path")
    .attr("class", function(d) { return "link " + d.type; })
    .attr("marker-end", function(d) { return "url(#" + d.type + ")"; });

var link = svg.selectAll(".link");

var node = svg.selectAll(".node")
    .data(force.nodes())
  .enter().append("g")
    .attr("class", "node")
    .call(force.drag).on("mouseover", fade(.1)).on("mouseout", fade(1));;

node.append("circle")
    .attr("r", (function(d) { return d.size;}))
    .style("fill", function (d) { if (d.size ==15) return '#339999'; else return '#660000'; });

node.append("text")
    .attr("x", 12)
    .attr("dy", ".35em")
    .style("font-size","14px")
    .text(function(d) { return d.name; });


// Use elliptical arc path segments to doubly-encode directionality.
function tick() {
  path.attr("d", linkArc);
  node.attr("transform", transform);
}



function linkArc(d) {
  var dx = d.target.x - d.source.x,
      dy = d.target.y - d.source.y,
      dr = Math.sqrt(dx * dx + dy * dy);
  return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
}

function transform(d) {
  return "translate(" + d.x + "," + d.y + ")";
}

function mouseover() {
    d3.select(this).select("circle").transition()
      .duration(50)
      .style("fill", '#033450');

}

function mouseout() {
  d3.select(this).select("circle").transition()
      .duration(50)
      .style("fill", function (d) { if (d.size ==15) return '#339999'; else return '#660000'; });
}

function fade(opacity) {
    return function(d) {
        node.style("stroke-opacity", function(o) {
            thisOpacity = isConnected(d, o) ? 1 : opacity;
            this.setAttribute('fill-opacity', thisOpacity);
            return thisOpacity;
        });

        link.style("stroke-opacity", function(o) {
            return o.source === d || o.target === d ? 1 : opacity;
        });

    };
}

});
};
});


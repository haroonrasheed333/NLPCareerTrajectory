var university = document.getElementById("university").value;
console.log(document.getElementById("university").value);

var skillsEmployer, univNumberMap;

$(document).ready(function () {

$("#inputs").empty;

if (university.length > 2) {
  var h3 = $('<h3>Displaying alumni network for all majors from your university. Key in your major to filter the network</h3><br>');
  var form = $('<form id="input-form"></form>');
  var major_div = $('<div class="column-33 column"><input type="text" name="major" id="major-ajax" style="position: relative; z-index: 2; background: transparent;"/></div>');
  var submit_button = $('<div class="column-25 column"><input id="tree-submit-button" class="btn btn-primary pull-right" type="submit" value="Re-create network" /></div>');

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
  var submit_button = $('<div class="column-25 column"><input id="tree-submit-button" class="btn btn-primary pull-right" type="submit" value="Create network" /></div>');

  $("#inputs").append(h3);
  form.append(univ_div);
  form.append(major_div);
  $("#inputs").append(form);
  $("#inputs").append(submit_button);

    // $("#inputs").append('<h3> Key in your university and major to generate your alumni network</h3></br>');
    // $("#inputs").append('<form id = "input-form"><div class="column-33 column"><input type="text" name="university" id="university-ajax" style="position: relative; z-index: 2; background: transparent;"/><input type = "hidden" type="text" name="university" id="university-ajax-x" disabled="disabled" style="color: #CCC; absolute: relative; background: transparent; z-index: 1;"/></div>')
    // $("#inputs").append('<div class="column-33 column"><input type="text" name="major" id="major-ajax" style="position: relative; z-index: 2; background: transparent;"/><input type = "hidden" type="text" name="country" id="major-ajax-x" disabled="disabled" style="color: #CCC; position: absolute; background: transparent; z-index: 1;"/></div>')
    // $("#inputs").append('<div class="column-25 column"><input id="tree-submit-button" class="btn btn-primary pull-right" type="subimt" value="Create network" style="position: absolute;" /></div></form>');
//    create_network();

}



 $("#tree-submit-button").on('click',function(){

    if (university.length > 2){
        var major_input = document.getElementById("major-ajax").value;

        $.ajax({
           datatype: 'json',
           url: '/submit',
           type: 'POST',
           data : {"major": JSON.stringify(document.getElementById("major-ajax").value)},
           success: function(data)
           {
               console.log(data);
               $("#tree-graph").remove();
               $("body").append($('<div id ="tree-graph" class = column-100></div>'));
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
               console.log(data);
               $("#tree-graph").remove();
               $("body").append($('<div id ="tree-graph" class="column-100"></div>'));
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

var diameter = 800;

var margin = {top: 20, right: 120, bottom: 20, left: 120},
    width = diameter,
    height = diameter;

var i = 0,
    duration = 350,
    root;

var tree = d3.layout.tree()
    .size([360, diameter*2 / 2 - 80])
    .separation(function(a, b) { return (a.parent == b.parent ? 1 : 10) / a.depth; });

var diagonal = d3.svg.diagonal.radial()
    .projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });

var svg = d3.select("#tree-graph").append("svg")
    .attr("width", width )
    .attr("height", height )
  .append("g")
    .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

d3.json("../static/treegraph.json", function(json) {
    root = json;
    root.x0 = height / 2;
    root.y0 = 0;

    //root.children.forEach(collapse); // start with all children collapsed
    update(root);

    d3.select(self.frameElement).style("height", "800px");

    function update(source) {

      // Compute the new tree layout.
      var nodes = tree.nodes(root),
          links = tree.links(nodes);

      // Normalize for fixed-depth.
      nodes.forEach(function(d) { d.y = d.depth * 80; });

      // Update the nodes…
      var node = svg.selectAll("g.node")
          .data(nodes, function(d) { return d.id || (d.id = ++i); });

      // Enter any new nodes at the parent's previous position.
      var nodeEnter = node.enter().append("g")
          .attr("class", "node")
          //.attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })
          .on("click", click);

      nodeEnter.append("circle")
          .attr("r", 1e-6)
          .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

      nodeEnter.append("text")
          .attr("x", 10)
          .attr("dy", ".35em")
          .attr("text-anchor", "start")
          //.attr("transform", function(d) { return d.x < 180 ? "translate(0)" : "rotate(180)translate(-" + (d.name.length * 8.5)  + ")"; })
          .text(function(d) { return d.name; })
          .style("fill-opacity", 1e-6);

      // Transition nodes to their new position.
      var nodeUpdate = node.transition()
          .duration(duration)
          .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

      nodeUpdate.select("circle")
          .attr("r", 4.5)
          .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

      nodeUpdate.select("text")
          .style("fill-opacity", 1)
          .attr("transform", function(d) { return d.x < 180 ? "translate(0)" : "rotate(180)translate(-" + (d.name.length + 50)  + ")"; });

      // TODO: appropriate transform
      var nodeExit = node.exit().transition()
          .duration(duration)
          //.attr("transform", function(d) { return "diagonal(" + source.y + "," + source.x + ")"; })
          .remove();

      nodeExit.select("circle")
          .attr("r", 1e-6);

      nodeExit.select("text")
          .style("fill-opacity", 1e-6);

      // Update the links…
      var link = svg.selectAll("path.link")
          .data(links, function(d) { return d.target.id; });

      // Enter any new links at the parent's previous position.
      link.enter().insert("path", "g")
          .attr("class", "link")
          .attr("d", function(d) {
            var o = {x: source.x0, y: source.y0};
            return diagonal({source: o, target: o});
          });

      // Transition links to their new position.
      link.transition()
          .duration(duration)
          .attr("d", diagonal);

      // Transition exiting nodes to the parent's new position.
      link.exit().transition()
          .duration(duration)
          .attr("d", function(d) {
            var o = {x: source.x, y: source.y};
            return diagonal({source: o, target: o});
          })
          .remove();

      // Stash the old positions for transition.
      nodes.forEach(function(d) {
        d.x0 = d.x;
        d.y0 = d.y;
      });
    }

    // Toggle children on click.
    function click(d) {
      if (d.children) {
        d._children = d.children;
        d.children = null;
      } else {
        d.children = d._children;
        d._children = null;
      }

      update(d);
    }

    // Collapse nodes
    function collapse(d) {
      if (d.children) {
          d._children = d.children;
          d._children.forEach(collapse);
          d.children = null;
        }
    }
    });




    //var w = 960,
    //    h = 2000,
    //    i = 0,
    //    duration = 500,
    //    root;
    //
    //var tree = d3.layout.tree()
    //    .size([h, w - 160]);
    //
    //var diagonal = d3.svg.diagonal()
    //    .projection(function(d) { return [d.y, d.x]; });
    //
    //var vis = d3.select("#tree-graph").append("svg:svg")
    //    .attr("width", w)
    //    .attr("height", h)
    //  .append("svg:g")
    //    .attr("transform", "translate(40,0)");
    //
    //d3.json("../static/treegraph.json", function(json) {
    //  json.x0 = 800;
    //  json.y0 = 0;
    //  update(root = json);
    //});
    //
    //function update(source) {
    //
    //  // Compute the new tree layout.
    //  var nodes = tree.nodes(root).reverse();
    // console.log(nodes)
    //  // Update the nodes…
    //  	var node = vis.selectAll("g.node")
    //      .data(nodes, function(d) { return d.id || (d.id = ++i); });
    //
    //	var nodeEnter = node.enter().append("svg:g")
    //    	.attr("class", "node")
    //    	.attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; });
    //    	//.style("opacity", 1e-6);
    //
    //  // Enter any new nodes at the parent's previous position.
    //
    //  	nodeEnter.append("svg:circle")
    //      //.attr("class", "node")
    //      //.attr("cx", function(d) { return source.x0; })
    //      //.attr("cy", function(d) { return source.y0; })
    //      .attr("r", 4.5)
    //      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; })
    //      .on("click", click);
    //
    //	nodeEnter.append("svg:text")
    //      	.attr("x", function(d) { return d._children ? -8 : 8; })
    //		.attr("y", 3)
    //      	//.attr("fill","#ccc")
    //      	//.attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
    //      	.text(function(d) { return d.name; });
    //
    //  // Transition nodes to their new position.
    //	nodeEnter.transition()
    //		.duration(duration)
    //		.attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
    //      	.style("opacity", 1)
    //      .select("circle")
    //    	//.attr("cx", function(d) { return d.x; })
    //		//.attr("cy", function(d) { return d.y; })
    //        .style("fill", "lightsteelblue");
    //
    //    node.transition()
    //      .duration(duration)
    //      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
    //      .style("opacity", 1);
    //
    //
    //	node.exit().transition()
    //      .duration(duration)
    //      .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
    //      .style("opacity", 1e-6)
    //      .remove();
    ///*
    //	var nodeTransition = node.transition()
    //		.duration(duration);
    //
    //  nodeTransition.select("circle")
    //      .attr("cx", function(d) { return d.y; })
    //      .attr("cy", function(d) { return d.x; })
    //      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });
    //
    //  nodeTransition.select("text")
    //      .attr("dx", function(d) { return d._children ? -8 : 8; })
    //	  .attr("dy", 3)
    //      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#5babfc"; });
    //
    //  // Transition exiting nodes to the parent's new position.
    //  var nodeExit = node.exit();
    //
    //  nodeExit.select("circle").transition()
    //      .duration(duration)
    //      .attr("cx", function(d) { return source.y; })
    //      .attr("cy", function(d) { return source.x; })
    //      .remove();
    //
    //  nodeExit.select("text").transition()
    //      .duration(duration)
    //      .remove();
    //*/
    //  // Update the links…
    //  var link = vis.selectAll("path.link")
    //      .data(tree.links(nodes), function(d) { return d.target.id; });
    //
    //  // Enter any new links at the parent's previous position.
    //  link.enter().insert("svg:path", "g")
    //      .attr("class", "link")
    //      .attr("d", function(d) {
    //        var o = {x: source.x0, y: source.y0};
    //        return diagonal({source: o, target: o});
    //      })
    //    .transition()
    //      .duration(duration)
    //      .attr("d", diagonal);
    //
    //  // Transition links to their new position.
    //  link.transition()
    //      .duration(duration)
    //      .attr("d", diagonal);
    //
    //  // Transition exiting nodes to the parent's new position.
    //  link.exit().transition()
    //      .duration(duration)
    //      .attr("d", function(d) {
    //        var o = {x: source.x, y: source.y};
    //        return diagonal({source: o, target: o});
    //      })
    //      .remove();
    //
    //  // Stash the old positions for transition.
    //  nodes.forEach(function(d) {
    //    d.x0 = d.x;
    //    d.y0 = d.y;
    //  });
    //}
    //
    //// Toggle children on click.
    //function click(d) {
    //  if (d.children) {
    //    d._children = d.children;
    //    d.children = null;
    //  } else {
    //    d.children = d._children;
    //    d._children = null;
    //  }
    //  update(d);
    //}
    //
    //d3.select(self.frameElement).style("height", "2000px");
    //
    //
    //
    //};

};
});








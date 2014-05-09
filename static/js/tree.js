var university = '';
$(document).ready(function () {

  $(window).load(function() {
        url_pathname = location.pathname;
        if (url_pathname == "/network") {
          university = document.getElementById("university").value;
          $("#inputs").empty;

          if (university.length > 2) {
            var h3 = $('<br><h3>Displaying top employers from your university first degree connections. Enter your major to personalize your results!</h3><br>');
            var form = $('<form id="input-form"></form>');
            var major_div = $('<div class="column"><input type="text" name="major" id="major-ajax" style="position: relative; z-index: 2;"/></div>');
            var submit_button = $('<div class="column"><input id="tree-submit-button" class="btn btn-primary pull-right" type="submit" value="Re-create network" /></div>');

            $("#inputs").append(h3);
            form.append(major_div);
            var form_div = $('<div id="network-input-div"></div>');
            form_div.append(form);
            form_div.append(submit_button);
            $("#inputs").append(form_div);

            $.ajax({
             datatype: 'json',
             url: '/get_tree',
             success: function(data)
             {
                 $("#tree-graph").remove();
                 $("body").append($('<div id ="tree-graph" class = column-100></div>'));
                 create_network(data);
             }
           });

          } else {

            var h3 = $('<br><h3>Enter you university and major to generate employers of your connections</h3><br>');
            var form = $('<form id="input-form"></form>');
            var univ_div = $('<div class="column"><input type="text" name="university" id="university-ajax" style="position: relative; z-index: 2;"/></div>');
            var major_div = $('<div class="column"><input type="text" name="major" id="major-ajax" style="position: relative; z-index: 2;"/></div>');
            var submit_button = $('<div class="column"><input id="tree-submit-button" class="btn btn-primary pull-right" type="submit" value="Create network" /></div><br><br>');

            $("#inputs").append(h3);
            form.append(univ_div);
            form.append(major_div);
            var form_div = $('<div id="network-input-div"></div>');
            form_div.append(form);
            form_div.append(submit_button);
            $("#inputs").append(form_div);

          }
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
               create_network(data);
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
               create_network(data);
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

function create_network(data) {


var margin = {top: 20, right: 80, bottom: 20, left: 80},
    width = 1200 - margin.right - margin.left,
    height = 1200 - margin.top - margin.bottom;

var i = 0,
    duration = 750,
    root;

var max = 0
var min = 0
var oldRange = 0
var newRange = 15
var newMin = 4

var tree = d3.layout.tree()
    .size([height, width]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });
$('#tree-graph').append('<h3>Click on the employers to view your second degree connection employers</h3></br>')
var svg = d3.select("#tree-graph").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// d3.json(data, function(error, flare) {
  root = $.parseJSON(data);
  root.x0 = height / 2;
  root.y0 = 0;


  function collapse(d) {
    if (d.children) {
      d._children = d.children;
      d._children.forEach(collapse);
      d.children = null;
    }
  }

  function maxMin(d){
      if (d.children){
          if (d.children.length > max){ max = d.children.length;}
          if (d.children.length < min){ min = d.children.length;}
      }
      else{
          if (d._children.length > max){ max = d._children.length;}
          if (d._children.length < min){ min = d._children.length;}
      }
  }
  root.children.forEach(maxMin);
  oldRange = max - min;
  root.children.forEach(collapse);
  update(root);

// });

d3.select(self.frameElement).style("height", "800px");

function update(source) {

  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse(),
      links = tree.links(nodes);

  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 180 * 2; });

  // Update the nodes…
  var node = svg.selectAll("g.node")
      .data(nodes, function(d) { return d.id || (d.id = ++i); });


  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node.enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
      .on("click", click)
      .on("mouseover", function(d) {
      if ((d._children) || (d.children)){
      var g = d3.select(this); // The node
      // The class is used to remove the additional text later
      var info = g.append('text')
         .classed('info', true)
         .attr('x', 20)
         .attr('y', 10)
         .text('');
      }
      })
      .on("mouseout", function(d) {
      // Remove the info text on mouse out.
      if ((d._children) || (d.children)){
      d3.select(this).select('text.info').remove();
      }
     });

  nodeEnter.append("circle")
      .attr("r", function(d) { return d._children ? (((d._children.length - min)*newRange/oldRange)+ newMin) : d.children? (((d.children.length - min)*newRange/oldRange)+ newMin) : 4; })
      .style("fill", function(d) { return d._children ? d._children.length != 0? "lightsteelblue" : "#fff" : d.children.length != 0? "lightsteelblue" : "#fff"; });

  nodeEnter.append("text")
    .attr("x", function(d) { return d._children ? 12 : -12; })
    .attr("y", 3)
    //.attr("fill","#ccc")
    //.attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
    .text(function(d) { return d.name; })
      .style("font-size","13px");

  // Transition nodes to their new position.
  var nodeUpdate = node.transition()
      .duration(duration)
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

  nodeUpdate.select("circle")
      .attr("r", function(d) { return d._children ? ((d._children.length - min)*newRange/oldRange)+ newMin: d.children ? ((d.children.length - min)*newRange/oldRange)+ newMin : 4; })
      .style("fill", function(d) { return d._children ? d._children.length != 0? "lightsteelblue" : "#fff" : d.children.length != 0? "lightsteelblue" : "#fff"; });

  nodeUpdate.select("text")
      .style("fill-opacity", 1);

  // Transition exiting nodes to the parent's new position.
  var nodeExit = node.exit().transition()
      .duration(duration)
      .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
      .remove();

  nodeExit.select("circle")
      .attr("r", function(d) { return d._children ? ((d._children.length - min)*newRange/oldRange)+ newMin: d.children ? ((d.children.length - min)*newRange/oldRange)+ newMin : 4; });

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

}

});

});





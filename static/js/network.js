//var countriesArray = $.map(countries, function (value, key) { return { value: value, data: key }; });

$(document).ready(function () {

create_network();
var majorsArray = [{ "value": "Education-Other"},
        { "value": "Anthropology"},
        { "value": "Nuclear Physics"},
        { "value": "Plant Sciences"},
        { "value": "Archaeology"}];

// Setup jQuery ajax mock:
$.mockjax({
    url: '*',
    responseTime: 2000,
    response: function (settings) {
        var query = settings.data.query,
            queryLowerCase = query.toLowerCase(),
            re = new RegExp('\\b' + $.Autocomplete.utils.escapeRegExChars(queryLowerCase), 'gi'),
            suggestions = $.grep(countriesArray, function (country) {
                 // return country.value.toLowerCase().indexOf(queryLowerCase) === 0;
                return re.test(country.value);
            }),
            response = {
                query: query,
                suggestions: suggestions
            };

        this.responseText = JSON.stringify(response);
    }
});

// Initialize ajax autocomplete:
$('#autocomplete-ajax').autocomplete({
    // serviceUrl: '/autosuggest/service/url',
    lookup: majorsArray,
    lookupFilter: function(suggestion, originalQuery, queryLowerCase) {
        var re = new RegExp('\\b' + $.Autocomplete.utils.escapeRegExChars(queryLowerCase), 'gi');
        return re.test(suggestion.value);
    },
    onSelect: function(suggestion) {
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
console.log(links);

var nodes = {};

// Compute the distinct nodes from the links.
links.forEach(function(link) {
  link.source = nodes[link.source] || (nodes[link.source] = {name: link.source, size: 15});
  link.target = nodes[link.target] || (nodes[link.target] = {name: link.target, size: 6});
});


var width = 960,
    height = 500;

var force = d3.layout.force()
    .nodes(d3.values(nodes))
    .links(links)
    .size([width, height])
    .gravity(.05)
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


/**
 * Created by Walter on 4/17/2015.
 */
function init_user_chart(){
    var width = 800,
    height = 250,
    height_full = height+40;

var y = d3.scale.linear()
    .range([height, 0]);

var chart = d3.select(".user-chart")
    .attr("width", width)
    .attr("height", height_full);
 d3.json("chart_data/user-counts.json", function(error, data) {
      data = data.sort(function(a,b){return b.count - a.count});
      data = data.map(function(a){
          return {label: a._id, value: a.count};
      });
      var total_count = data.reduce(function(a,b){
          return {value: a.value + b.value};
      }).value;
      data = data.slice(0,7);
      y.domain([0, d3.max(data, function(d) { return d.value; })+40]);

      var barWidth = width / data.length;

      var bar = chart.selectAll("g")
          .data(data)
        .enter().append("g")
          .attr("transform", function(d, i) { return "translate(" + i * barWidth + ",0)"; });

      bar.append("rect")
          .attr("y", function(d) { return y(d.value); })
          .attr("height", function(d) { return height - y(d.value); })
          .attr("width", barWidth - 1);

      bar.append("text")
          .attr("x", barWidth / 2)
          .attr("y", function(d) { return height+3; })
          .attr("dy", "0.75em")
          .attr("class", "axis")
          .text(function(d) { return d.label+": "+ d.value; });

      bar.append("text")
          .attr("x", barWidth/2)
          .attr("y", function(d) {
              if (height-28 < y(d.value/2))
                return height-28;
              else
                return y(d.value/2);
              })
          .attr("dy", "1.5em")
          .text(function(d) { return (d.value/total_count*100).toFixed(0) + "%"; });

     bar.selectAll("text.axis").call(wrap, barWidth / 2)
    });
    chart.append("text")
          .attr("x", 500)
          .attr("y", 50)
          .attr("dy", "1.5em")
          .text(">[{$group:{_id:\"$created.user\",count:{$sum:1}}}, {$sort:{count:-1}}]");
}

function init_elem_chart() {
    var width = 240,
    height = 240,
    radius = Math.min(width, height) / 2;

    var color = d3.scale.ordinal()
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

    var arc = d3.svg.arc()
        .outerRadius(radius - 30)
        .innerRadius(0);

    var pie = d3.layout.pie()
        .sort(null)
        .value(function(d) { return d.value; });

    var svg = d3.select(".elem-chart")
        .attr("width", width+50)
        .attr("height", height+50)
      .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

      var data = [{"label":"node", value:319347},
                    {"label":"relation", value:600},
                    {"label":"way",value:51319},
                    {label:"nd", value:397853},
                    {label:"tag", value:118598},
                    {label:"member", value:5066}];
      data.forEach(function(d) {
      var elem_color = color(d.value);
      var elems = d3.select("."+ d.label).style("color", elem_color);
      var g = svg.selectAll(".arc")
          .data(pie(data))
        .enter().append("g")
          .attr("class", "arc");

      g.append("path")
          .attr("d", arc)
          .style("fill", function(d) { return color(d.value); });
      var pos = d3.svg.arc().innerRadius(radius-20).outerRadius(radius-5);
      g.append("text")
          .attr("transform", function(d) { return "translate(" + pos.centroid(d) + ")"; })
          .attr("dy", ".35em")
          .style("text-anchor", "start")
          .text(function(d){return d.data.label;})
          .style("fill", function(d){return color(d.value);});
    });

}

function wrap(text, width) {
  text.each(function() {
      var text = d3.select(this),
          words = text.text().split(/\s+/).reverse(),
          word,
          line = [],
          lineNumber = 0,
          lineHeight = 1.1, // ems
          y = text.attr("y"),
          dy = parseFloat(text.attr("dy")),
          tspan = text.text(null).append("tspan").attr("x", width).attr("y", y).attr("dy", dy + "em");
      while (word = words.pop()) {
          line.push(word);
          tspan.text(line.join(" "));
          if (tspan.node().getComputedTextLength() > 2 * width && width !=0) {
              line.pop();
              tspan.text(line.join(" "));
              line = [word];
              tspan = text.append("tspan").attr("x", width).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
          } else if (width == 0){
          }
      }
  });
}
  
/**
 * Created by Walter on 4/17/2015.
 */
function init_user_chart(){
    var width = 800,
    height = 300,
    height_full = height+40;

var y = d3.scale.linear()
    .range([height, 0]);

var chart = d3.select(".chart")
    .attr("width", width)
    .attr("height", height_full);
 d3.json("chart_data/user-counts.json", function(error, data) {
      data = data.sort(function(a,b){return b.count - a.count}).slice(0,7);
      data = data.map(function(a){return {label: a._id, value: a.count}});
      y.domain([0, d3.max(data, function(d) { return d.value; })+40]);
     console.log(data);

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
          .text(function(d) { return d.label+" "+ d.value; });

     bar.selectAll("text").call(wrap, barWidth / 2)
    });
}

function wrap(text, width) {
  text.each(function() {
    console.log(d3.select(this).attr("dy"));
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
      if (tspan.node().getComputedTextLength() > 2*width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", width).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      }
    }
  });
}
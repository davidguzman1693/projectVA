// For chart2

  var x2 = d3version4.scaleBand()
      .rangeRound([0, width])
      .padding([0.5]);

  var y2 = d3version4.scaleLinear()
      .range([height, 0]);

  var xAxis2 = d3version4.axisBottom()
      .scale(x2);

  var yAxis2 =  d3version4.axisLeft()
      .scale(y2);

  var svg2 = d3version4.select("#chart2").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var dict2 = []

  //Jaccard
  var outerJac = d3version3.map();
  var innerJac = [];
  var linksJac = [];

  var outerIdJac = [0];

  conceMap2 = [];

  d3version3.csv("clustered.csv", function(error, dataframe) {
      dataframe.forEach(function(d) {
      
      if(!(d.Jackcluster in dict2)){
        dict2[d.Jackcluster] = 0;
      }else{
        dict2[d.Jackcluster] = dict2[d.Jackcluster] + 1;
      }

      if(!(d.Jackcluster in conceMap2)){
        conceMap2[d.Jackcluster] = d.important.split(" ");
      }else{
        var s = conceMap2[d.Jackcluster];
        var t = d.important.split(" ");
        s.push.apply(s, t)
        conceMap2[d.Jackcluster] = s;
      } 
    });

    //Second cluster
    x2.domain(dataframe.map(function(d) { return d.Jackcluster; }));
    //y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
    y2.domain([0, d3version4.max(dataframe, function(d) { return dict2[d.Jackcluster]; })]);

    svg2.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis2);

    svg2.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Number of tweets");

    svg2.selectAll(".bar")
        .data(dataframe)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x2(d.Jackcluster); })
        .attr("width", x2.bandwidth())
        .attr("y", function(d) { return y2(dict2[d.Jackcluster]); })
        //.attr("height", function(d) { return height - y(dict[d.clusterd]); })
        .attr("height", function(d) { return height - y2(dict2[d.Jackcluster]); })
        .attr("selected",false)
        .on("click", function(d,i){
            console.log(d.Jackcluster) // Cluster of tweet
            // Remove active class from all buttons
            if (d3version4.select(this).attr("selected") === "false")
              {
              d3version4.select(this)
              .attr("selected",true)
                .style("fill","yellow")
                refVector.push(i);
                datVector.push(d.frequency);
                console.log(datVector)
            }
            else
            {
                d3version4.select(this)
              .attr("selected",false)
                .style("fill","steelblue")
                var index=refVector.indexOf(i)
                console.log(index)
                refVector.splice(index,1);
                datVector.splice(index,1);
                console.log(datVector)
            }
        });

    d3version4.select("input").on("change", change);

    

    function change() {
      clearTimeout(sortTimeout);

      // Copy-on-write since tweens are evaluated after a delay.
      var x0 = x.domain(data.sort(this.checked
          ? function(a, b) { return b.frequency - a.frequency; }
          : function(a, b) { return d3version4.ascending(a.letter, b.letter); })
          .map(function(d) { return d.letter; }))
          .copy();

      svg.selectAll(".bar")
          .sort(function(a, b) { return x0(a.letter) - x0(b.letter); });

      var transition = svg.transition().duration(750),
          delay = function(d, i) { return i * 50; };

      transition.selectAll(".bar")
          .delay(delay)
          .attr("x", function(d) { return x0(d.letter); });

      transition.select(".x.axis")
          .call(xAxis)
        .selectAll("g")
          .delay(delay);
    }
  });

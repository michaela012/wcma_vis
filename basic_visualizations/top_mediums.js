// set the dimensions and margins of the graph
var margin = {left:50, right:50, top:40, bottom:0};
    width = 600,
    height = 500;

// set the ranges
var x = d3.scaleBand()
          .range([0, width])
          .padding(.5);
var y = d3.scaleLinear()
          .range([height, 1.0]);
          
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("body").append("svg")
    .attr("width", "100%") //width + margin.left + margin.right)
    .attr("height", "100%") //height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");

// get the data
d3.csv("top_mediums.csv", function(error, data) {
  if (error) throw error;

  // format the data
  data.forEach(function(d) {
    d.count = +d.count;
  });

  // Scale the range of the data in the domains
  x.domain(data.map(function(d) { return d.medium; }));
  y.domain([0, d3.max(data, function(d) { return d.count; })]);

  // append the rectangles for the bar chart
  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("fill","green")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.medium); })
      .attr("width", x.bandwidth())
      .attr("y", function(d) { return y(d.count); })
      .attr("height", function(d) { return height - y(d.count); });

  // add the x Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))//;
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" );

  // add the y Axis
  svg.append("g")
      .call(d3.axisLeft(y));

});













/*

d3.csv("top_mediums.csv")
  .row(function(d){ return {medium: d.medium, count: Number(d.count.trim())}; })
  .get(function(error, data){
    var height = 300;
    var width = 500;

  var x = d3.scaleOrdinal().range([0,width], .05);
  var y = d3.scaleLinear().range([height, 0]);

  var svg = d3.select("body").append("svg")
    .attr("height", "100%")
    .attr("width", "100%");

  var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    //.tickFormat()

  var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(20);
  
  var margin = {left:50, right:50, top:40, bottom:0};
  
  var chartGroup = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  x.domain(data.map(function(d){ return d.medium; } ));
  y.domain([0, d3.max(data, function(d){ return d.count; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("trasform", "translate(0," + height + ")")
      .call(xAxis)
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" );
    
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Value ($)");

  svg.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .style("fill", "steelblue")
      .attr("x", function(d) { return x(d.medium); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.count); })
      .attr("height", function(d) { return height - y(d.value); });


  });






/*

    var max = d3.max(data, function(d){ return d.count; });
    
    var x = d3.scaleLinear()
      .domain([0,max])
      .range([0, width]);
    var y = d3.scaleLinear()
      .domain([0, max])
      .range([height, 0]);

    var yAxis = d3.axisLeft(y);
    var xAxis = d3.axisBottom(x);


    var svg = d3.select("body").append("svg").attr("height","100%").attr("width", "100%");
    var margin = {left:50, right:50, top:40, bottom:0};
  
    var chartGroup = svg.append("g")
      .attr("transform","translate("+margin.left+","+margin.top+")");

    var line = d3.line()
      .x(function(d){ return x(d.count); })
      .y(function(d){ return y(d.count); });

    chartGroup.append("path").attr("d",line(data));

    //console.log(data);

}); 

/*
var parseDate = d3.timeParse("%m/%d/%Y");

d3.csv("prices.csv")
    .row(function(d){ return {month: parseDate(d.month), price:Number(d.price.trim().slice(1))}; })
    .get(function(error,data){

      var height = 300;
      var width = 500;

      var max = d3.max(data,function(d){ return d.price; });
      var minDate = d3.min(data,function(d){ return d.month; });
      var maxDate = d3.max(data,function(d){ return d.month; });

      var y = d3.scaleLinear()
                  .domain([0,max])
                  .range([height,0]);
      var x = d3.scaleTime()
                  .domain([minDate,maxDate])
                  .range([0,width]);
      var yAxis = d3.axisLeft(y);
      var xAxis = d3.axisBottom(x);

      var svg = d3.select("body").append("svg").attr("height","100%").attr("width","100%");

      var margin = {left:50,right:50,top:40,bottom:0};

      var chartGroup = svg.append("g")
                  .attr("transform","translate("+margin.left+","+margin.top+")");

      var line = d3.line()
                      .x(function(d){ return x(d.month); })
                      .y(function(d){ return y(d.price); });

      chartGroup.append("path").attr("d",line(data));
      chartGroup.append("g").attr("class","x axis").attr("transform","translate(0,"+height+")").call(xAxis);
      chartGroup.append("g").attr("class","y axis").call(yAxis);
    })

    */
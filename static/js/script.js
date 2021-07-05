/**
 * ---------------------------------------
 * This demo was created using amCharts 4.
 * 
 * For more information visit:
 * https://www.amcharts.com/
 * 
 * Documentation is available at:
 * https://www.amcharts.com/docs/v4/
 * ---------------------------------------
 */

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

// Create chart instance
var chart = am4core.create("chartdiv", am4charts.PieChart);
chart.startAngle = 160;
chart.endAngle = 380;

// Let's cut a hole in our Pie chart the size of 40% the radius
chart.innerRadius = am4core.percent(40);

// Add data
chart.data = [{
  "country": "Lithuania",
  "litres": 501.9,
  "bottles": 1500
}, {
  "country": "Czech Republic",
  "litres": 301.9,
  "bottles": 990
}, {
  "country": "Ireland",
  "litres": 201.1,
  "bottles": 785
}, {
  "country": "Germany",
  "litres": 165.8,
  "bottles": 255
}, {
  "country": "Australia",
  "litres": 139.9,
  "bottles": 452
}, {
  "country": "Austria",
  "litres": 128.3,
  "bottles": 332
}, {
  "country": "UK",
  "litres": 99,
  "bottles": 150
}, {
  "country": "Belgium",
  "litres": 60,
  "bottles": 178
}, {
  "country": "The Netherlands",
  "litres": 50,
  "bottles": 50
}];

// Add and configure Series
var pieSeries = chart.series.push(new am4charts.PieSeries());
pieSeries.dataFields.value = "litres";
pieSeries.dataFields.category = "country";
pieSeries.slices.template.stroke = new am4core.InterfaceColorSet().getFor("background");
pieSeries.slices.template.strokeWidth = 1;
pieSeries.slices.template.strokeOpacity = 1;

// Disabling labels and ticks on inner circle
pieSeries.labels.template.disabled = true;
pieSeries.ticks.template.disabled = true;

// Disable sliding out of slices
pieSeries.slices.template.states.getKey("hover").properties.shiftRadius = 0;
pieSeries.slices.template.states.getKey("hover").properties.scale = 1;
pieSeries.radius = am4core.percent(40);
pieSeries.innerRadius = am4core.percent(30);

var cs = pieSeries.colors;
cs.list = [am4core.color(new am4core.ColorSet().getIndex(0))];

cs.stepOptions = {
  lightness: -0.05,
  hue: 0
};
cs.wrap = false;


// Add second series
var pieSeries2 = chart.series.push(new am4charts.PieSeries());
pieSeries2.dataFields.value = "bottles";
pieSeries2.dataFields.category = "country";
pieSeries2.slices.template.stroke = new am4core.InterfaceColorSet().getFor("background");
pieSeries2.slices.template.strokeWidth = 1;
pieSeries2.slices.template.strokeOpacity = 1;
pieSeries2.slices.template.states.getKey("hover").properties.shiftRadius = 0.05;
pieSeries2.slices.template.states.getKey("hover").properties.scale = 1;

pieSeries2.labels.template.disabled = true;
pieSeries2.ticks.template.disabled = true;


var label = chart.seriesContainer.createChild(am4core.Label);
label.textAlign = "middle";
label.horizontalCenter = "middle";
label.verticalCenter = "middle";
label.adapter.add("text", function(text, target){
	return "[font-size:18px]total[/]:\n[bold font-size:30px]" + pieSeries.dataItem.values.value.sum + "[/]";
})
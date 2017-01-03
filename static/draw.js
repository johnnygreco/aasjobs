Chart.defaults.Line.bezierCurve = false; // straight line between points
Chart.defaults.Line.multiTooltipTemplate = "<%= datasetLabel %> - <%= value %>";

var nlines = 0;
var data, myNewChart, searchword;
var ctx = $("#yearCount").get(0).getContext("2d");

$(document).ready(function () {

  $("button#clear").click(function () {
    myNewChart.destroy();
    nlines = 0;
  });

  ctx.canvas.onclick = function (e) {
    var activePoint = myNewChart.getPointsAtEvent(e)[0];
    var table = $('<table></table>');
    for (var i = 0, len = 3; i < len; i++) {
      var row = $('<tr><td>a</td><td>b</td></tr>');
      table.append(row);
    }
    $("div#listing").append(table);
  };

  $("form").submit(function (e) {
    e.preventDefault();
    searchword = $("#searchbox").val();
    if ( nlines == 0 ) {
      $.get('/search', {keyword: searchword}, function(d) {
        data = jQuery.parseJSON(d);
        myNewChart = new Chart(ctx).Line(data, {datasetFill: false});
      });
      nlines += 1;
    } else {
      searchword = $("#searchbox").val();
      $.get('/search', {keyword: searchword}, function(d) {
        var tmpdata = jQuery.parseJSON(d).datasets[0];
        console.log(data);
        data.datasets.push(tmpdata);
        myNewChart.destroy();
        myNewChart = new Chart(ctx).Line(data, {datasetFill: false, animation: false});
      });
      nlines += 1;
    }
  });
});



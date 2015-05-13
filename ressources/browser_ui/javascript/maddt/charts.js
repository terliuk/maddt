
$(document).ready(function(){
var data = {
    labels : ["January","February","March","April","May","June","July","August","September","October","November","December"],
    datasets : [
        {
            fillColor : "rgba(220,220,220,0.5)",
            strokeColor : "rgba(220,220,220,1)",
            data : [1,2,3,4,5,6,7,8,9,10,11,12]
        },
        {
            fillColor : "rgba(151,187,205,0.5)",
            strokeColor : "rgba(151,187,205,1)",
            data : [1,2,3,4,5,6,7,8,9,10,11,12]
        }
    ]
}
var ctx = document.getElementById("myChart").getContext("2d");
//var ctx = $("#totalcopy").get(0).getContext("2d");
new Chart(ctx).Bar(data,options);
});
